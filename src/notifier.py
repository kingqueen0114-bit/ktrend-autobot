import os
import hmac
import hashlib
import requests
import json
from typing import Dict
from utils.logging_config import log_event, log_error

class Notifier:
    def __init__(self, access_token: str, user_id: str):
        self.access_token = access_token
        self.user_id = user_id
        self.api_url = "https://api.line.me/v2/bot/message/push"

    def send_error_notification(self, error_type: str, error_message: str, context: str = ""):
        """
        Send error notification to LINE for monitoring.

        Args:
            error_type: Type of error (e.g., "API_ERROR", "PARSE_ERROR")
            error_message: Error details
            context: Additional context
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        # Parse User IDs
        if "," in self.user_id:
            user_ids = [uid.strip() for uid in self.user_id.split(",") if uid.strip()]
            api_endpoint = "https://api.line.me/v2/bot/message/multicast"
            recipient_payload = {"to": user_ids}
        else:
            api_endpoint = "https://api.line.me/v2/bot/message/push"
            recipient_payload = {"to": self.user_id}

        # Truncate message if too long
        error_message = error_message[:500] if len(error_message) > 500 else error_message

        flex_message = {
            "type": "flex",
            "altText": f"K-Trend エラー通知: {error_type}",
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "⚠️ K-Trend エラー通知", "weight": "bold", "size": "lg", "color": "#FF5722"},
                        {"type": "separator", "margin": "md"},
                        {"type": "text", "text": f"種類: {error_type}", "size": "sm", "margin": "md", "color": "#666666"},
                        {"type": "text", "text": error_message, "wrap": True, "size": "xs", "margin": "sm", "color": "#999999"},
                        {"type": "text", "text": f"コンテキスト: {context}", "wrap": True, "size": "xs", "margin": "md", "color": "#999999"} if context else {"type": "filler"}
                    ]
                }
            }
        }

        payload = {
            **recipient_payload,
            "messages": [flex_message]
        }

        try:
            response = requests.post(api_endpoint, headers=headers, data=json.dumps(payload))
            log_event("LINE_ERROR_NOTIFICATION_SENT", "Error notification sent", status_code=response.status_code)
        except Exception as e:
            log_error("LINE_ERROR_NOTIFICATION_FAILED", "Failed to send error notification", error=e)

    def send_progress_report(self, project_name: str, status: str, completed_tasks: list, next_tasks: list, notes: str = ""):
        """
        Send autonomous development progress report.

        Args:
            project_name: Name of the project
            status: Current status
            completed_tasks: List of completed tasks
            next_tasks: List of upcoming tasks
            notes: Additional notes
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        # Parse User IDs
        if "," in self.user_id:
            user_ids = [uid.strip() for uid in self.user_id.split(",") if uid.strip()]
            api_endpoint = "https://api.line.me/v2/bot/message/multicast"
            recipient_payload = {"to": user_ids}
        else:
            api_endpoint = "https://api.line.me/v2/bot/message/push"
            recipient_payload = {"to": self.user_id}

        # Build task lists
        completed_text = "\n".join([f"✅ {t}" for t in completed_tasks[:5]]) if completed_tasks else "なし"
        next_text = "\n".join([f"📋 {t}" for t in next_tasks[:3]]) if next_tasks else "なし"

        flex_message = {
            "type": "flex",
            "altText": f"進捗報告: {project_name}",
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"📊 進捗報告: {project_name}", "weight": "bold", "size": "lg", "color": "#1DB446"},
                        {"type": "separator", "margin": "md"},
                        {"type": "text", "text": f"ステータス: {status}", "size": "sm", "margin": "md", "weight": "bold"},
                        {"type": "text", "text": "完了タスク:", "size": "sm", "margin": "lg", "color": "#666666"},
                        {"type": "text", "text": completed_text, "wrap": True, "size": "xs", "margin": "sm", "color": "#999999"},
                        {"type": "text", "text": "次回予定:", "size": "sm", "margin": "lg", "color": "#666666"},
                        {"type": "text", "text": next_text, "wrap": True, "size": "xs", "margin": "sm", "color": "#999999"},
                        {"type": "text", "text": f"備考: {notes}", "wrap": True, "size": "xs", "margin": "lg", "color": "#888888"} if notes else {"type": "filler"}
                    ]
                }
            }
        }

        payload = {
            **recipient_payload,
            "messages": [flex_message]
        }

        try:
            response = requests.post(api_endpoint, headers=headers, data=json.dumps(payload))
            log_event("LINE_PROGRESS_REPORT_SENT", "Progress report sent", status_code=response.status_code)
            return response.status_code == 200
        except Exception as e:
            log_error("LINE_PROGRESS_REPORT_FAILED", "Failed to send progress report", error=e)
            return False

    def _send_custom_messages(self, messages: list) -> bool:
        """
        Send custom raw messages to the configured LINE users.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        
        if "," in self.user_id:
            user_ids = [uid.strip() for uid in self.user_id.split(",") if uid.strip()]
            api_endpoint = "https://api.line.me/v2/bot/message/multicast"
            recipient_payload = {"to": user_ids}
        else:
            api_endpoint = "https://api.line.me/v2/bot/message/push"
            recipient_payload = {"to": self.user_id}
            
        payload = {
            **recipient_payload,
            "messages": messages
        }
        
        try:
            response = requests.post(api_endpoint, headers=headers, data=json.dumps(payload))
            log_event("LINE_CUSTOM_MESSAGES_SENT", "Custom messages sent", status_code=response.status_code)
            return response.status_code == 200
        except Exception as e:
            log_error("LINE_CUSTOM_MESSAGES_FAILED", "Failed to send custom messages", error=e)
            return False

    def _validate_image_url(self, url: str) -> str:
        """
        Validate and return a working image URL for LINE Flex Messages.
        LINE requires HTTPS URLs that return actual image data.

        Returns:
            A validated HTTPS image URL or a fallback placeholder
        """
        # Curated fallback images that always work
        fallback_images = [
            "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop",  # Concert
            "https://images.unsplash.com/photo-1517154421773-0529f29ea451?w=600&h=400&fit=crop",  # Seoul
            "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=600&h=400&fit=crop",  # Cosmetics
        ]

        # Check if URL is valid
        if not url or not isinstance(url, str):
            log_event("IMAGE_URL_MISSING", "No image URL provided, using fallback")
            return fallback_images[0]

        # Must be HTTPS for LINE
        if not url.startswith("https://"):
            log_event("IMAGE_URL_NOT_HTTPS", "Image URL not HTTPS, using fallback", url_prefix=url[:50])
            return fallback_images[0]

        # Skip placeholder URLs
        if "placeholder" in url.lower() or "example.com" in url:
            log_event("IMAGE_URL_PLACEHOLDER", "Placeholder URL detected, using fallback")
            return fallback_images[0]

        # Quick HEAD request to validate URL (with timeout)
        try:
            response = requests.head(url, timeout=5, allow_redirects=True, headers={
                "User-Agent": "Mozilla/5.0 (compatible; K-Trend-Bot/1.0)"
            })
            if response.status_code == 200:
                content_type = response.headers.get("Content-Type", "")
                if "image" in content_type or url.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
                    return url
                else:
                    log_event("IMAGE_URL_INVALID_TYPE", "URL is not an image", content_type=content_type)
            else:
                log_event("IMAGE_URL_BAD_STATUS", "Image URL returned non-200 status", status_code=response.status_code)
        except requests.exceptions.Timeout:
            log_event("IMAGE_URL_TIMEOUT", "Image URL timeout, using as-is", url_prefix=url[:50])
            return url  # Still try to use it
        except Exception as e:
            log_error("IMAGE_URL_VALIDATION_FAILED", "Image URL validation failed", error=e)

        # Return fallback
        import random
        return random.choice(fallback_images)

    def send_trend_preview(self, trends: list, preview_id: str) -> bool:
        """トレンドプレビューをCarousel Flex Messageで送信"""
        import random
        from urllib.parse import urlparse

        category_emojis = {
            'artist': '🎤', 'beauty': '💄', 'fashion': '👗',
            'food': '🍜', 'travel': '✈️', 'event': '🎉',
            'drama': '📺', 'other': '📰', 'trend': '🔥'
        }

        bubbles = []
        for idx, trend in enumerate(trends[:10]):  # Carousel最大10バブル
            title = trend.get('title', '不明')[:40]
            snippet = trend.get('snippet', '')[:80]
            category = trend.get('category', 'trend')
            emoji = category_emojis.get(category, '📰')
            image_url = self._validate_image_url(trend.get('image_url', ''))
            link = trend.get('link', '')

            # ソースドメイン表示
            try:
                domain = urlparse(link).netloc if link else ''
            except Exception:
                domain = ''

            # Postbackデータ: 300バイト制限に注意
            postback_data = f"action=gen_from_preview&idx={idx}&pid={preview_id}"

            # body contents
            body_contents = [
                {
                    "type": "text",
                    "text": f"{emoji} {category.upper()}",
                    "size": "xs",
                    "color": "#0277BD",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": title,
                    "weight": "bold",
                    "size": "sm",
                    "wrap": True,
                    "maxLines": 2,
                    "margin": "sm"
                },
                {
                    "type": "text",
                    "text": snippet + "..." if snippet else "（詳細なし）",
                    "size": "xs",
                    "color": "#888888",
                    "wrap": True,
                    "maxLines": 3,
                    "margin": "sm"
                },
            ]

            if domain:
                body_contents.append({
                    "type": "text",
                    "text": f"📎 {domain}",
                    "size": "xxs",
                    "color": "#aaaaaa",
                    "margin": "md"
                })

            # footer buttons
            footer_contents = [
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "color": "#1DB446",
                    "action": {
                        "type": "postback",
                        "label": "📝 この記事を生成",
                        "data": postback_data,
                        "displayText": f"「{title[:20]}」を記事生成します"
                    }
                },
            ]

            if link:
                footer_contents.append({
                    "type": "button",
                    "style": "secondary",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "🔗 ソースを見る",
                        "uri": link
                    }
                })

            bubble = {
                "type": "bubble",
                "size": "kilo",
                "hero": {
                    "type": "image",
                    "url": image_url,
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": body_contents
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": footer_contents
                }
            }
            bubbles.append(bubble)

        # 「全て生成」バブル（トレンド2件以上の場合）
        if len(trends) >= 2:
            gen_all_postback = f"action=gen_all_preview&pid={preview_id}"
            all_bubble = {
                "type": "bubble",
                "size": "kilo",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "contents": [
                        {"type": "text", "text": "🚀", "size": "3xl", "align": "center"},
                        {"type": "text", "text": f"全{len(trends)}件を生成", "weight": "bold", "size": "md", "align": "center", "margin": "lg"},
                        {"type": "text", "text": "すべてのトレンドから\n記事を一括生成します", "size": "xs", "color": "#888888", "align": "center", "wrap": True, "margin": "md"}
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#FF5722",
                            "action": {
                                "type": "postback",
                                "label": f"🚀 全{len(trends)}件を生成",
                                "data": gen_all_postback,
                                "displayText": f"全{len(trends)}件のトレンドから記事を生成します"
                            }
                        }
                    ]
                }
            }
            bubbles.append(all_bubble)

        carousel = {
            "type": "flex",
            "altText": f"🔥 トレンドプレビュー {len(trends)}件",
            "contents": {
                "type": "carousel",
                "contents": bubbles
            }
        }

        return self._send_custom_messages([carousel])

    def send_approval_request(self, content: Dict, image_url: str, draft_id: str = None, wp_post_id: int = None, wp_preview_url: str = None, quality_data: Dict = None, additional_images: list = None, slug: str = None):
        """
        Sends a Flex Message with an Approval Button (Postback) to one or multiple users.

        Args:
            content: コンテンツデータ
            image_url: 画像URL
            draft_id: FirestoreのドラフトID
            wp_post_id: WordPressの投稿ID（下書き）
            wp_preview_url: WordPressのプレビューURL
            quality_data: 品質チェック結果 {'score': int, 'passed': bool, 'warnings': list, 'was_rewritten': bool}
            additional_images: 追加画像URLのリスト
        """
        news_post = content.get('news_post', 'N/A')
        luna_a = content.get('luna_post_a', 'Luna投稿A')
        luna_b = content.get('luna_post_b', 'Luna投稿B')

        # Validate and get working image URL
        validated_image_url = self._validate_image_url(image_url)
        log_event("IMAGE_URL_SELECTED", "Using validated image URL", url_prefix=validated_image_url[:60])

        # Prepare CMS data display if available
        cms_title = content.get('title', '')

        # Build quality score section if available
        quality_section = []
        if quality_data:
            score = quality_data.get('score', 0)
            passed = quality_data.get('passed', False)
            warnings = quality_data.get('warnings', [])
            was_rewritten = quality_data.get('was_rewritten', False)

            # Score color based on value
            if score >= 80:
                score_color = "#1DB446"  # Green
                score_emoji = "🟢"
            elif score >= 60:
                score_color = "#FFA000"  # Amber
                score_emoji = "🟡"
            else:
                score_color = "#F44336"  # Red
                score_emoji = "🔴"

            # Quality score display
            quality_section.append({"type": "separator", "margin": "md"})
            quality_section.append({
                "type": "box",
                "layout": "horizontal",
                "margin": "md",
                "contents": [
                    {"type": "text", "text": f"{score_emoji} 品質スコア", "size": "sm", "color": "#666666", "flex": 2},
                    {"type": "text", "text": f"{score}/100", "size": "sm", "weight": "bold", "color": score_color, "align": "end", "flex": 1}
                ]
            })

            # Rewritten indicator
            if was_rewritten:
                quality_section.append({
                    "type": "text",
                    "text": "🔄 自動リライト済み",
                    "size": "xs",
                    "color": "#0277BD",
                    "margin": "sm"
                })

            # Warnings (show first 2)
            if warnings and not passed:
                warning_text = " / ".join(warnings[:2])
                quality_section.append({
                    "type": "text",
                    "text": f"⚠️ {warning_text}",
                    "size": "xs",
                    "color": "#FF6F00",
                    "wrap": True,
                    "margin": "sm"
                })

        # Action Data - WordPressのpost_idも含める
        postback_data = f"action=approve&draft_id={draft_id}"
        if wp_post_id:
            postback_data += f"&wp_post_id={wp_post_id}"

        # Pre-calculate URIs for buttons (Next.js frontend)
        next_app_url = os.environ.get("NEXT_APP_URL", "https://k-trendtimes.com")
        edit_secret = os.environ.get("EDIT_SECRET", "")
        preview_secret = os.environ.get("PREVIEW_SECRET", "")

        # HMAC token for edit URL authentication
        edit_token = hmac.new(edit_secret.encode(), draft_id.encode(), hashlib.sha256).hexdigest() if edit_secret else ""
        edit_uri = f"{next_app_url}/edit/{draft_id}?token={edit_token}"

        # Preview URL (uses Next.js API preview route)
        cms_slug = slug or content.get('slug', draft_id)
        preview_uri = f"{next_app_url}/api/preview?slug={cms_slug}&secret={preview_secret}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        
        log_event("LINE_APPROVAL_REQUEST_SENDING", "Sending approval notification")
        
        # Parse User IDs (Handle single or comma-separated list)
        if "," in self.user_id:
            user_ids = [uid.strip() for uid in self.user_id.split(",") if uid.strip()]
            is_multicast = True
            api_endpoint = "https://api.line.me/v2/bot/message/multicast"
            recipient_payload = {"to": user_ids}
        else:
            user_ids = [self.user_id]
            is_multicast = False
            api_endpoint = "https://api.line.me/v2/bot/message/push"
            recipient_payload = {"to": self.user_id}

        # Category emoji mapping
        category_emojis = {
            'artist': '🎤', 'beauty': '💄', 'fashion': '👗',
            'food': '🍜', 'travel': '✈️', 'event': '🎉',
            'drama': '📺', 'other': '📰', 'trend': '🔥'
        }
        category = content.get('category', 'trend')
        category_emoji = category_emojis.get(category, '📰')

        # Build body contents - simplified (details available on view_draft page)
        body_contents = [
            {"type": "text", "text": "📰 K-Trend 新着記事", "weight": "bold", "size": "xl", "color": "#1DB446"},
            {"type": "text", "text": cms_title, "wrap": True, "size": "md", "weight": "bold", "margin": "md"},
            {
                "type": "box",
                "layout": "horizontal",
                "margin": "sm",
                "contents": [
                    {"type": "text", "text": f"{category_emoji} {category.upper()}", "size": "xs", "color": "#0277BD", "weight": "bold"},
                ]
            },
            {"type": "text", "text": "「📖 記事を開く」で全文確認・編集・公開ができます", "wrap": True, "size": "xs", "color": "#999999", "margin": "md"}
        ]

        # Add quality section if available
        if quality_section:
            body_contents.extend(quality_section)

        # Add Research Report (Signs Analysis) if available
        research_report = content.get('research_report')
        if research_report:
            body_contents.append({"type": "separator", "margin": "lg"})
            body_contents.append({
                "type": "text", 
                "text": "🔍 【AIリサーチ報告】流行のサイン", 
                "weight": "bold", 
                "size": "sm", 
                "color": "#FF5722", 
                "margin": "lg"
            })
            body_contents.append({
                "type": "text", 
                "text": research_report, 
                "wrap": True, 
                "size": "xs", 
                "color": "#666666", 
                "margin": "sm"
            })

        # Add image count if there are additional images
        if additional_images and len(additional_images) > 0:
            total_images = 1 + len(additional_images)  # Main image + additional
            body_contents.append({"type": "separator", "margin": "md"})
            body_contents.append({
                "type": "box",
                "layout": "horizontal",
                "margin": "md",
                "contents": [
                    {"type": "text", "text": "🖼️ 画像", "size": "sm", "color": "#666666", "flex": 2},
                    {"type": "text", "text": f"{total_images}枚", "size": "sm", "weight": "bold", "color": "#0277BD", "align": "end", "flex": 1}
                ]
            })

        # Flex Message (Enhanced with content preview and Approve/Reject buttons)
        flex_message = {
            "type": "flex",
            "altText": "K-Trend 承認リクエスト",
            "contents": {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": validated_image_url,
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": body_contents
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "height": "sm",
                                    "color": "#1DB446",
                                    "action": {
                                        "type": "postback",
                                        "label": "✅ 承認",
                                        "data": postback_data,
                                        "displayText": "承認しました"
                                    }
                                },
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "height": "sm",
                                    "action": {
                                        "type": "uri",
                                        "label": "✏️ 編集",
                                        "uri": edit_uri
                                    }
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "button",
                                    "style": "secondary",
                                    "height": "sm",
                                    "action": {
                                        "type": "uri",
                                        "label": "👁️ プレビュー",
                                        "uri": preview_uri
                                    }
                                },
                                {
                                    "type": "button",
                                    "style": "secondary",
                                    "height": "sm",
                                    "action": {
                                        "type": "postback",
                                        "label": "❌ 却下",
                                        "data": f"action=reject&draft_id={draft_id}",
                                        "displayText": "却下しました"
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        }
        
        payload = {
            **recipient_payload,
            "messages": [flex_message]
        }

        try:
            response = requests.post(api_endpoint, headers=headers, data=json.dumps(payload))
            log_event("LINE_API_RESPONSE", "LINE API response received", status_code=response.status_code)
            response.raise_for_status()
        except Exception as e:
            log_error("LINE_FLEX_MESSAGE_FAILED", "Flex message sending failed", error=e)
            # Fallback (Simple broadcast might be better than fail)
            pass

    def send_stats_summary(self, stats: Dict, period_days: int = 7, best_articles: list = None) -> bool:
        """
        Send weekly/periodic statistics summary to LINE.

        Args:
            stats: Statistics data from get_stats_summary()
            period_days: Number of days in the period
            best_articles: List of best performing articles from get_best_articles()

        Returns:
            True if sent successfully
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        # Parse User IDs
        if "," in self.user_id:
            user_ids = [uid.strip() for uid in self.user_id.split(",") if uid.strip()]
            api_endpoint = "https://api.line.me/v2/bot/message/multicast"
            recipient_payload = {"to": user_ids}
        else:
            api_endpoint = "https://api.line.me/v2/bot/message/push"
            recipient_payload = {"to": self.user_id}

        # Extract stats
        total_trends = stats.get('total_trends', 0)
        total_drafts = stats.get('total_drafts', 0)
        official_images = stats.get('official_images', 0)
        fallback_images = stats.get('fallback_images', 0)
        image_rate = stats.get('official_image_rate', 0)
        days_collected = stats.get('days_collected', 0)
        categories = stats.get('categories', {})
        approved_count = stats.get('approved_count', 0)
        rejected_count = stats.get('rejected_count', 0)
        approval_rate = stats.get('approval_rate', 0)

        # Performance stats
        total_published = stats.get('total_published', 0)
        avg_quality_score = stats.get('avg_quality_score', 0)
        rewritten_count = stats.get('rewritten_count', 0)
        scheduled_count = stats.get('scheduled_count', 0)

        # Build category display (top 4 categories)
        category_emojis = {
            'artist': '🎤', 'beauty': '💄', 'fashion': '👗',
            'food': '🍜', 'travel': '✈️', 'event': '🎉',
            'drama': '📺', 'other': '📰', 'trend': '🔥'
        }
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:4]
        category_text = " / ".join([f"{category_emojis.get(c, '📰')}{c}:{n}" for c, n in sorted_categories]) if sorted_categories else "データなし"

        # Determine status color/emoji
        if image_rate >= 80:
            status_emoji = "🟢"
            status_text = "良好"
        elif image_rate >= 50:
            status_emoji = "🟡"
            status_text = "普通"
        else:
            status_emoji = "🔴"
            status_text = "要改善"

        # Build body contents dynamically
        body_contents = [
            {"type": "text", "text": "📊 K-Trend 統計レポート", "weight": "bold", "size": "lg", "color": "#1DB446"},
            {"type": "text", "text": f"直近{period_days}日間の統計", "size": "xs", "color": "#999999", "margin": "sm"},
            {"type": "separator", "margin": "md"},
            {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "📈 取得トレンド数", "size": "sm", "color": "#666666", "flex": 2},
                            {"type": "text", "text": f"{total_trends}件", "size": "sm", "weight": "bold", "align": "end", "flex": 1}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "📝 作成記事数", "size": "sm", "color": "#666666", "flex": 2},
                            {"type": "text", "text": f"{total_drafts}件", "size": "sm", "weight": "bold", "align": "end", "flex": 1}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "🖼️ 公式画像取得", "size": "sm", "color": "#666666", "flex": 2},
                            {"type": "text", "text": f"{official_images}件", "size": "sm", "weight": "bold", "align": "end", "flex": 1}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "📷 代替画像使用", "size": "sm", "color": "#666666", "flex": 2},
                            {"type": "text", "text": f"{fallback_images}件", "size": "sm", "weight": "bold", "align": "end", "flex": 1}
                        ]
                    }
                ]
            },
            {"type": "separator", "margin": "lg"},
            {
                "type": "box",
                "layout": "horizontal",
                "margin": "lg",
                "contents": [
                    {"type": "text", "text": f"{status_emoji} 公式画像率", "size": "sm", "color": "#666666", "flex": 2},
                    {"type": "text", "text": f"{image_rate:.1f}% ({status_text})", "size": "sm", "weight": "bold", "align": "end", "flex": 2}
                ]
            },
            {"type": "separator", "margin": "lg"},
            {
                "type": "box",
                "layout": "horizontal",
                "margin": "lg",
                "contents": [
                    {"type": "text", "text": "✅ 承認率", "size": "sm", "color": "#666666", "flex": 2},
                    {"type": "text", "text": f"{approval_rate:.0f}% ({approved_count}承認/{rejected_count}却下)", "size": "xs", "weight": "bold", "align": "end", "flex": 3}
                ]
            },
            {"type": "separator", "margin": "lg"},
            {"type": "text", "text": "📈 パフォーマンス", "weight": "bold", "size": "sm", "color": "#666666", "margin": "lg"},
            {
                "type": "box",
                "layout": "vertical",
                "margin": "sm",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "公開済み記事", "size": "xs", "color": "#888888", "flex": 2},
                            {"type": "text", "text": f"{total_published}件", "size": "xs", "weight": "bold", "align": "end", "flex": 1}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "平均品質スコア", "size": "xs", "color": "#888888", "flex": 2},
                            {"type": "text", "text": f"{avg_quality_score}/100", "size": "xs", "weight": "bold", "align": "end", "flex": 1, "color": "#1DB446" if avg_quality_score >= 70 else "#FFA000"}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "自動リライト", "size": "xs", "color": "#888888", "flex": 2},
                            {"type": "text", "text": f"{rewritten_count}件", "size": "xs", "weight": "bold", "align": "end", "flex": 1}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "予約公開待ち", "size": "xs", "color": "#888888", "flex": 2},
                            {"type": "text", "text": f"{scheduled_count}件", "size": "xs", "weight": "bold", "align": "end", "flex": 1}
                        ]
                    }
                ]
            },
            {"type": "separator", "margin": "lg"},
            {"type": "text", "text": "📂 カテゴリ内訳", "size": "sm", "color": "#666666", "margin": "lg"},
            {"type": "text", "text": category_text, "size": "xs", "color": "#0277BD", "margin": "sm", "wrap": True}
        ]

        # Add best articles section if available
        if best_articles and len(best_articles) > 0:
            body_contents.append({"type": "separator", "margin": "lg"})
            body_contents.append({"type": "text", "text": "🏆 週間ベスト記事", "weight": "bold", "size": "sm", "color": "#FF6F00", "margin": "lg"})

            for i, article in enumerate(best_articles[:3], 1):
                title = article.get('title', '無題')[:30]
                if len(article.get('title', '')) > 30:
                    title += "..."
                score = article.get('score', 0)
                category = article.get('category', 'trend')
                cat_emoji = category_emojis.get(category, '📰')

                # Medal emoji for ranking
                medal = ['🥇', '🥈', '🥉'][i-1] if i <= 3 else f"{i}."

                body_contents.append({
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "sm",
                    "contents": [
                        {"type": "text", "text": f"{medal} {cat_emoji}", "size": "xs", "flex": 0},
                        {"type": "text", "text": title, "size": "xs", "color": "#555555", "flex": 4, "wrap": True},
                        {"type": "text", "text": f"{score}点", "size": "xs", "color": "#1DB446", "weight": "bold", "align": "end", "flex": 1}
                    ]
                })

        # Add footer note
        body_contents.append({"type": "text", "text": f"※ {days_collected}日分のデータを集計", "size": "xs", "color": "#aaaaaa", "margin": "lg"})

        flex_message = {
            "type": "flex",
            "altText": f"K-Trend 週間統計レポート",
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": body_contents
                }
            }
        }

        payload = {
            **recipient_payload,
            "messages": [flex_message]
        }

        try:
            response = requests.post(api_endpoint, headers=headers, data=json.dumps(payload))
            log_event("LINE_STATS_SUMMARY_SENT", "Stats summary sent", status_code=response.status_code)
            return response.status_code == 200
        except Exception as e:
            log_error("LINE_STATS_SUMMARY_FAILED", "Failed to send stats summary", error=e)
            return False

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    uid = os.getenv("LINE_USER_ID")
    
    if token and uid:
        notifier = Notifier(token, uid)
        mock_content = {
            "title": "Mock Title",
            "news_post": "NEWS: Test post.",
            "luna_post_a": "LUNA A: So cute!",
            "luna_post_b": "LUNA B: Buy this."
        }
        # Use a reliable HTTPS image for test
        mock_img = "https://via.placeholder.com/300" 
        notifier.send_approval_request(mock_content, mock_img, "test_draft_id")
    else:
        log_event("LINE_CREDENTIALS_MISSING", "LINE credentials not found in environment")
