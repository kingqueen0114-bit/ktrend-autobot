"""
Scheduler handler functions for K-Trend AutoBot.
Triggered by Cloud Scheduler for daily fetch, stats reports, and progress reports.
"""
import os
import functions_framework

from src.fetch_trends import TrendFetcher
from src.content_generator import ContentGenerator, check_article_quality
from src.notifier import Notifier
from src.storage_manager import StorageManager
from utils.logging_config import log_event, log_error


@functions_framework.http
def trigger_daily_fetch(request):
    """
    Cron Job Entry Point.
    1. Fetches Trends (Random + KPOP)
    2. Generates SNS & CMS Drafts for each
    3. Saves to Firestore
    4. Sends LINE "Approve" Button
    """
    import time
    from datetime import datetime

    start_time = time.time()
    log_event("DAILY_FETCH_START", "Starting daily fetch process")

    # Init Components
    fetcher = TrendFetcher(os.environ.get("GEMINI_API_KEY"))
    generator = ContentGenerator(os.environ.get("GEMINI_API_KEY"))
    notifier = Notifier(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"), os.environ.get("LINE_USER_ID"))
    storage = StorageManager()

    # Statistics tracking
    stats = {
        'total_trends': 0,
        'total_drafts': 0,
        'official_images': 0,
        'fallback_images': 0,
        'categories': {}
    }
    errors = []

    # Fetch trends with KPOP included (limit to 4 for faster processing)
    trends = fetcher.fetch_trends(include_kpop=True)
    if trends and len(trends) > 4:
        log_event("TREND_LIMITING", f"Limiting from {len(trends)} to 4 for faster processing")
        trends = trends[:4]

    # Filter out duplicate trends (already published in last 24 hours)
    if trends:
        original_count = len(trends)
        trends = [t for t in trends if not storage.is_duplicate_trend(t.get('title', ''))]
        if len(trends) < original_count:
            log_event("TREND_DUPLICATE_FILTER", f"Filtered {original_count - len(trends)} duplicate trends, {len(trends)} new trends remaining")

    # Cleanup old trend titles periodically
    storage.cleanup_old_trend_titles(days=7)

    if not trends:
        log_event("TREND_NOT_FOUND", "No trends found, exiting")
        try:
            notifier.send_error_notification(
                error_type="NO_TRENDS_FOUND",
                error_message="トレンドが見つかりませんでした",
                context="定期実行でトレンドが0件でした"
            )
        except:
            pass
        return "No trends", 200

    stats['total_trends'] = len(trends)

    # Process each trend
    draft_ids = []
    for idx, target in enumerate(trends):
        log_event("TREND_PROCESSING", f"Processing {idx + 1}/{len(trends)}", trend_title=target.get('title', 'Unknown'))

        try:
            # Track category
            category = target.get('category', 'other')
            stats['categories'][category] = stats['categories'].get(category, 0) + 1

            # Track image source
            if 'Unsplash' in target.get('image_source', ''):
                stats['fallback_images'] += 1
            else:
                stats['official_images'] += 1

            # Generate SNS
            sns_content = generator.generate_content(target)
            # Generate CMS (with Signs Context)
            trend_sign_context = target.get('snippet', '')
            cms_content = generator.generate_cms_article(target, trend_sign_context=trend_sign_context)

            # Quality check
            quality = check_article_quality(cms_content, target)
            log_event("QUALITY_CHECK", f"Quality score: {quality['score']}/100 ({'PASS' if quality['passed'] else 'WARN'})", score=quality['score'], passed=quality['passed'])
            if quality['warnings']:
                for warn in quality['warnings'][:3]:
                    log_event("QUALITY_WARNING", warn)

            # Auto-rewrite if quality is too low (Strict Self-Correction Loop)
            rewritten = False
            rewrite_attempts = 0
            max_rewrites = 3
            
            while not quality['passed'] and rewrite_attempts < max_rewrites:
                rewrite_attempts += 1
                log_event("ARTICLE_REWRITE", f"Auto-rewriting article (Attempt {rewrite_attempts}/{max_rewrites}) due to rule violations")
                cms_content = generator.rewrite_article(cms_content, quality['warnings'], target, trend_sign_context=trend_sign_context)
                
                # Re-check quality after rewrite
                quality = check_article_quality(cms_content, target)
                log_event("QUALITY_CHECK", f"After rewrite {rewrite_attempts}: {quality['score']}/100 ({'PASS' if quality['passed'] else 'WARN'})", score=quality['score'], passed=quality['passed'], rewrite_attempt=rewrite_attempts)
                
                if quality['warnings']:
                    for warn in quality['warnings'][:3]:
                        log_event("QUALITY_WARNING", warn, rewrite_attempt=rewrite_attempts)
                rewritten = True

            # Save to WordPress as draft first
            img_url = target.get('image_url')
            additional_images = target.get('additional_images', [])
            trend_category = target.get('category', 'other')
            # Extract artist_tags from generated content
            artist_tags = cms_content.get('artist_tags', [])
            if artist_tags:
                target['artist_tags'] = artist_tags
                log_event("ARTIST_TAGS_EXTRACTED", f"Artist tags extracted: {artist_tags}", tags=artist_tags)
            wp_result = storage.save_draft_to_wordpress(cms_content, img_url, additional_images, trend_category, artist_tags)

            # Save Draft to Firestore (with WordPress info and quality score)
            draft_data = {
                "status": "draft",
                "trend_source": target,
                "sns_content": sns_content,
                "cms_content": cms_content,
                "quality_score": quality['score'],
                "quality_passed": quality['passed'],
                "quality_warnings": quality['warnings'],
                "was_rewritten": rewritten,
                "wordpress_post_id": wp_result["id"] if wp_result else None,
                "wordpress_preview_url": wp_result.get("preview_url") if wp_result else None,
            }
            draft_id = storage.save_draft(draft_data)
            draft_ids.append(draft_id)
            stats['total_drafts'] += 1

            # Save trend title for duplicate detection
            storage.save_trend_title(target.get('title', ''), {'draft_id': draft_id, 'category': category})

            # Send Approval Request for this draft with quality data
            notifier.send_approval_request(
                content={**sns_content, **cms_content},
                image_url=img_url,
                draft_id=draft_id,
                wp_post_id=wp_result["id"] if wp_result else None,
                wp_preview_url=wp_result.get("preview_url") if wp_result else None,
                quality_data={
                    'score': quality['score'],
                    'passed': quality['passed'],
                    'warnings': quality['warnings'],
                    'was_rewritten': rewritten
                },
                additional_images=additional_images,
                slug=wp_result.get("slug") if wp_result else None
            )
        except Exception as e:
            error_msg = f"Error processing trend {idx + 1}: {str(e)}"
            log_error("TREND_PROCESSING_ERROR", error_msg, error=e,
                      trend_title=target.get('title', 'Unknown')[:50])
            errors.append(error_msg)
            # Send immediate error notification for individual trend failures
            try:
                notifier.send_error_notification(
                    error_type="TREND_PROCESSING_ERROR",
                    error_message=str(e),
                    context=f"Trend {idx + 1}: {target.get('title', 'Unknown')[:50]}"
                )
            except:
                pass  # Don't fail if error notification fails

    # Calculate execution time
    duration = time.time() - start_time

    # Log execution
    execution_log = {
        'timestamp': datetime.now().isoformat(),
        'trends_fetched': stats['total_trends'],
        'drafts_created': stats['total_drafts'],
        'official_images': stats['official_images'],
        'fallback_images': stats['fallback_images'],
        'errors': errors,
        'duration_seconds': round(duration, 2)
    }
    storage.log_execution(execution_log)

    # Update daily stats
    today = datetime.now().strftime('%Y-%m-%d')
    storage.update_daily_stats(today, stats)

    # Send error summary notification if there were errors
    if errors:
        try:
            notifier.send_error_notification(
                error_type="DAILY_FETCH_ERRORS",
                error_message=f"{len(errors)}件のエラーが発生しました",
                context=f"成功: {stats['total_drafts']}件 / 失敗: {len(errors)}件"
            )
        except:
            pass

    log_event("DAILY_FETCH_COMPLETE", f"Processed {len(draft_ids)} trends in {duration:.1f}s",
              stats=stats, duration_ms=int(duration * 1000), draft_ids=draft_ids)
    return f"Success: {len(draft_ids)} drafts created", 200


@functions_framework.http
def trigger_stats_report(request):
    """
    Weekly/Periodic Statistics Report Entry Point.
    Triggered by Cloud Scheduler to send statistics summary to LINE.
    Includes GA4 analytics report if GA4_PROPERTY_ID is configured.
    """
    log_event("STATS_REPORT_START", "Starting stats report generation")

    try:
        notifier = Notifier(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"), os.environ.get("LINE_USER_ID"))
        storage = StorageManager()

        # Get weekly stats (7 days)
        stats = storage.get_stats_summary(days=7)
        log_event("STATS_SUMMARY", "Stats summary retrieved", stats=stats)

        # Get best articles for the week
        best_articles = storage.get_best_articles(days=7, limit=3)
        log_event("BEST_ARTICLES", f"Best articles retrieved: {len(best_articles)} articles", count=len(best_articles))

        # Send to LINE
        success = notifier.send_stats_summary(stats, period_days=7, best_articles=best_articles)

        # GA4 Analytics Report (if configured)
        ga4_property_id = os.environ.get("GA4_PROPERTY_ID")
        if ga4_property_id:
            try:
                from src.analytics_reporter import AnalyticsReporter, ReportScheduler
                analytics = AnalyticsReporter(ga4_property_id)
                scheduler = ReportScheduler(analytics, notifier)
                scheduler.send_weekly_report()
                log_event("GA4_REPORT_SENT", "GA4 weekly report sent successfully")
            except Exception as ga4_err:
                log_error("GA4_REPORT_ERROR", f"GA4 report failed (non-critical): {str(ga4_err)}", error=ga4_err)
        else:
            log_event("GA4_REPORT_SKIP", "GA4_PROPERTY_ID not configured, skipping analytics report")

        if success:
            return "Stats report sent successfully", 200
        else:
            return "Failed to send stats report", 500

    except Exception as e:
        log_error("STATS_REPORT_ERROR", "Stats report generation failed", error=e)
        return f"Error: {str(e)}", 500


@functions_framework.http
def trigger_progress_report(request):
    """
    Development Progress Report Entry Point.
    Can be triggered to send progress reports via LINE.

    Expected JSON payload:
    {
        "action": "progress_report",
        "project_name": "K-Trend AutoBot",
        "status": "完了" | "進行中" | "エラー",
        "completed_tasks": ["タスク1", "タスク2"],
        "next_tasks": ["次のタスク1"],
        "notes": "追加メモ"
    }
    """
    log_event("PROGRESS_REPORT_START", "Starting progress report generation")

    try:
        import json as json_lib

        # Parse request body
        data = {}
        if request.is_json:
            data = request.get_json(silent=True) or {}
        elif request.method == 'POST' and request.data:
            try:
                data = json_lib.loads(request.data.decode('utf-8'))
            except (json_lib.JSONDecodeError, UnicodeDecodeError):
                pass

        # Extract parameters
        project_name = data.get('project_name', 'K-Trend AutoBot')
        status = data.get('status', '完了')
        completed_tasks = data.get('completed_tasks', [])
        next_tasks = data.get('next_tasks', [])
        notes = data.get('notes', '')

        notifier = Notifier(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"), os.environ.get("LINE_USER_ID"))

        # Send progress report
        success = notifier.send_progress_report(
            project_name=project_name,
            status=status,
            completed_tasks=completed_tasks,
            next_tasks=next_tasks,
            notes=notes
        )

        if success:
            return "Progress report sent successfully", 200
        else:
            return "Failed to send progress report", 500

    except Exception as e:
        log_error("PROGRESS_REPORT_ERROR", "Progress report generation failed", error=e)
        return f"Error: {str(e)}", 500


@functions_framework.http
def trigger_sync_view_counts(request):
    """GA4のPVデータをSanityのviewCountフィールドに同期"""
    import src.sanity_client as sanity_client
    from src.analytics_reporter import AnalyticsReporter
    from datetime import datetime, timedelta

    property_id = os.environ.get("GA4_PROPERTY_ID")
    if not property_id:
        return ("GA4_PROPERTY_ID not configured", 500)

    try:
        reporter = AnalyticsReporter(property_id)
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        top_pages = reporter.get_top_pages(start_date, end_date, limit=50)

        # /articles/{slug} または /notes/{slug}（旧WPパス）からslugを抽出
        article_views = {}
        for page in top_pages:
            path = page.get("path", "")
            slug = None
            if path.startswith("/articles/"):
                slug = path.replace("/articles/", "").strip("/")
            elif path.startswith("/notes/"):
                slug = path.replace("/notes/", "").strip("/")
            if slug:
                # 同一slugの重複はPV合算
                article_views[slug] = article_views.get(slug, 0) + page.get("page_views", 0)

        if not article_views:
            return ("No article page views found", 200)

        # Sanityの記事IDをslugから取得
        slugs = list(article_views.keys())
        query = '*[_type == "article" && slug.current in $slugs]{ _id, "slug": slug.current }'
        articles = sanity_client.query(query, {"slugs": slugs})

        # バッチでviewCountを更新
        mutations = []
        updated = 0
        for article in articles:
            slug = article.get("slug")
            if slug in article_views:
                mutations.append({
                    "patch": {
                        "id": article["_id"],
                        "set": {"viewCount": article_views[slug]}
                    }
                })
                updated += 1

        if mutations:
            sanity_client.transaction(mutations)

        msg = f"ViewCount synced: {updated} articles updated"
        print(msg)
        return (msg, 200)

    except Exception as e:
        print(f"ViewCount sync error: {e}")
        return (f"Error: {str(e)}", 500)
