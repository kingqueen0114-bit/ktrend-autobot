"""
Draft editor handler for K-Trend AutoBot.
Redirects to Next.js edit page, handles legacy POST approval/publishing.
"""
import os
import hmac
import hashlib
import functions_framework
from datetime import datetime
import json

from jinja2 import Environment, FileSystemLoader

from src.storage_manager import StorageManager
from utils.logging_config import log_event, log_error

# Jinja2 template engine initialization (kept for result pages)
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def render_template(template_name, **context):
    """Render a Jinja2 template with the given context."""
    template = jinja_env.get_template(template_name)
    return template.render(**context)


@functions_framework.http
def view_draft(request):
    """
    HTTP endpoint to display draft content as HTML form for editing and approval.
    Handles both GET (view/edit) and POST (approve/publish).
    URL: /view_draft?id=DRAFT_ID
    """
    draft_id = request.args.get('id')
    if not draft_id:
        return "<h1>Error: No draft ID provided</h1>", 400

    storage = StorageManager()
    draft = storage.get_draft(draft_id)

    if not draft:
        return "<h1>Error: Draft not found or expired</h1>", 404

    # --- POST Request: Process Approval & Publishing ---
    if request.method == 'POST':
        form = request.form

        # --- AJAX Image Upload Logic ---
        if form.get('action') == 'upload_image':
            uploaded_file = request.files.get('file')
            if not uploaded_file:
                return json.dumps({"error": "No file uploaded"}), 400, {'Content-Type': 'application/json'}

            try:
                storage = StorageManager()
                image_bytes = uploaded_file.read()
                content_type = uploaded_file.content_type or 'image/jpeg'
                uploaded_url = storage.upload_bytes_to_gcs(image_bytes, content_type)

                if uploaded_url:
                    log_event("INLINE_IMAGE_UPLOADED", f"Inline image uploaded: {uploaded_file.filename}")
                    return json.dumps({"url": uploaded_url}), 200, {'Content-Type': 'application/json'}
                else:
                    return json.dumps({"error": "Upload failed"}), 500, {'Content-Type': 'application/json'}
            except Exception as e:
                log_error("INLINE_IMAGE_UPLOAD_ERROR", str(e))
                return json.dumps({"error": str(e)}), 500, {'Content-Type': 'application/json'}

        # --- Normal Form Submission Logic ---

        # 1. Update Content with Edited Validation
        # CMS
        cms_content = draft.get('cms_content', {})
        if 'approve_cms' in form:
            cms_content['title'] = form.get('cms_title', '')
            cms_content['body'] = form.get('cms_body', '')
            cms_content['meta_description'] = form.get('cms_meta', '')
            cms_content['x_post_1'] = form.get('x_post_1', '')
            cms_content['x_post_2'] = form.get('x_post_2', '')

        # SNS
        sns_content = draft.get('sns_content', {})
        sns_to_publish = {}

        if 'approve_news' in form:
            sns_content['news_post'] = form.get('news_post', '')
            sns_to_publish['news_post'] = sns_content['news_post']

        if 'approve_luna_a' in form:
            sns_content['luna_post_a'] = form.get('luna_post_a', '')
            sns_to_publish['luna_post_a'] = sns_content['luna_post_a']

        if 'approve_luna_b' in form:
            sns_content['luna_post_b'] = form.get('luna_post_b', '')
            sns_to_publish['luna_post_b'] = sns_content['luna_post_b']

        # 2. Handle Image URL (check if changed)
        new_image_url = form.get('image_url', '').strip()
        original_image_url = draft.get('trend_source', {}).get('image_url', '')

        # Handle file upload first
        uploaded_file = request.files.get('image_file')
        if uploaded_file and uploaded_file.filename:
            try:
                image_bytes = uploaded_file.read()
                content_type = uploaded_file.content_type or 'image/jpeg'
                uploaded_url = storage.upload_bytes_to_gcs(image_bytes, content_type)
                if uploaded_url:
                    new_image_url = uploaded_url
                    log_event("IMAGE_UPLOADED", f"File uploaded: {uploaded_file.filename}")
            except Exception as e:
                log_event("IMAGE_UPLOAD_ERROR", str(e))

        # Use new image URL if provided and different
        if new_image_url and new_image_url != original_image_url:
            img_url = new_image_url
            # Update trend_source with new image
            if 'trend_source' not in draft:
                draft['trend_source'] = {}
            draft['trend_source']['image_url'] = new_image_url
            log_event("IMAGE_CHANGED", f"Image URL updated to: {new_image_url[:50]}...")
        else:
            img_url = original_image_url

        # Save image source/credit (always save from form)
        new_image_source = form.get('image_source', '').strip()
        if new_image_source:
            if 'trend_source' not in draft:
                draft['trend_source'] = {}
            draft['trend_source']['image_source'] = new_image_source

        # 2.5 Handle Category
        new_category = form.get('category', 'trend')
        if 'trend_source' not in draft:
            draft['trend_source'] = {}
        draft['trend_source']['category'] = new_category

        # 2.6 Handle Artist Tags
        artist_tags_str = form.get('artist_tags', '').strip()
        artist_tags = [tag.strip() for tag in artist_tags_str.split(',') if tag.strip()] if artist_tags_str else []
        draft['trend_source']['artist_tags'] = artist_tags
        log_event("CATEGORY_TAGS_UPDATE", f"Category: {new_category}, Tags: {artist_tags}")

        # 3. Save updated draft to Firestore and handle action
        action_type = form.get('action_type', 'publish')
        draft['cms_content'] = cms_content
        draft['sns_content'] = sns_content

        if action_type == 'save_draft':
            draft['status'] = 'pending'
            storage.save_draft(draft, draft_id)
            return render_template('result.html',
                title='保存完了',
                icon='💾',
                heading_color='#0277bd',
                bg_color='#e3f2fd',
                message='下書きとして保存しました。LINEの「下書き」メニューから確認できます。',
                sub_message=None,
                url=None,
                links=[{'href': 'https://line.me/R/', 'label': '💬 LINEに戻る', 'style': 'secondary', 'target': None}]
            ), 200

        draft['status'] = 'approved'
        storage.save_draft(draft, draft_id)

        # 4. Publish to Sanity if CMS is approved
        if 'approve_cms' in form:
            # Sanity移行: draft_idを使用して公開
            sanity_draft_id = draft.get('sanity_draft_id') or draft_id
            wp_post_id = draft.get('wordpress_post_id') or draft.get('wordpress_id')
            result = storage.publish_to_wordpress(cms_content, img_url, category=new_category, artist_tags=artist_tags, wp_post_id=wp_post_id, draft_id=sanity_draft_id)
            if result:
                draft['wordpress_url'] = result['url']
                draft['wordpress_id'] = result['id']
                storage.save_draft(draft, draft_id)

                # Success page with link
                return render_template('result.html',
                    title='公開完了！',
                    icon='🎉',
                    heading_color='#1DB446',
                    bg_color='#e8f5e9',
                    message='記事が公開されました。',
                    sub_message=None,
                    url=result['url'],
                    links=[
                        {'href': result['url'], 'label': '📰 記事を確認', 'style': None, 'target': '_blank'},
                        {'href': 'https://line.me/R/', 'label': '💬 LINEに戻る', 'style': 'secondary', 'target': None}
                    ]
                ), 200
            else:
                return render_template('result.html',
                    title='公開エラー',
                    icon='❌',
                    heading_color='#f44336',
                    bg_color='#ffebee',
                    message='記事の公開に失敗しました。',
                    sub_message='しばらく待ってから再度お試しください。',
                    url=None,
                    links=[{'href': 'javascript:history.back()', 'label': '← 戻る', 'style': 'outline', 'target': None}]
                ), 500
        else:
            return render_template('result.html',
                title='保存完了',
                icon='✅',
                heading_color='#1DB446',
                bg_color='#e8f5e9',
                message='修正内容は保存されました。',
                sub_message='（CMSにチェックがなかったため、公開されていません）',
                url=None,
                links=[{'href': 'javascript:history.back()', 'label': '← 戻る', 'style': 'outline', 'target': None}]
            ), 200

    # --- GET Request: Redirect to Next.js edit page ---
    next_app_url = os.environ.get("NEXT_APP_URL", "https://k-trendtimes.com")
    edit_secret = os.environ.get("EDIT_SECRET", "")

    # Generate HMAC token for edit page authentication
    edit_token = hmac.new(edit_secret.encode(), draft_id.encode(), hashlib.sha256).hexdigest() if edit_secret else ""
    edit_url = f"{next_app_url}/edit/{draft_id}?token={edit_token}"

    log_event("VIEW_DRAFT_REDIRECT", f"Redirecting to Next.js edit page", draft_id=draft_id)

    # 302 redirect to Next.js edit page
    return "", 302, {"Location": edit_url}

def view_article_list(request):
    """
    HTTP endpoint to display a list of drafts and published articles.
    URL: /drafts?tab=pending (default) or /drafts?tab=published
    """
    tab = request.args.get('tab', 'pending')
    storage = StorageManager()

    # Query logic based on tab
    if tab == 'pending':
        query = storage.db.collection(storage.collection_name).where('status', 'in', ['draft', 'pending'])
    elif tab == 'published':
        query = storage.db.collection(storage.collection_name).where('status', 'in', ['approved', 'published'])
    else:
        query = storage.db.collection(storage.collection_name).where('status', 'in', ['draft', 'pending'])

    # Sort and execute
    query = query.order_by('created_at', direction='DESCENDING').limit(50)
    docs = list(query.stream())

    # Build article data list for template
    articles = []
    category_names = {
        'artist': 'K-POP', 'beauty': '美容', 'fashion': '服',
        'food': 'グルメ', 'travel': '旅行', 'event': 'イベント',
        'drama': 'ドラマ', 'trend': 'トレンド', 'other': 'その他'
    }

    for doc in docs:
        draft = doc.to_dict()
        draft_id = doc.id
        cms_content = draft.get('cms_content', {})
        title = cms_content.get('title', '無題')
        trend_source = draft.get('trend_source', {})
        category = trend_source.get('category', 'trend')

        created_at = draft.get('created_at')
        date_str = ""
        if created_at:
            try:
                date_str = created_at.strftime("%Y-%m-%d %H:%M")
            except:
                date_str = str(created_at)

        cat_display = category_names.get(category, 'トレンド')

        articles.append({
            'draft_id': draft_id,
            'title': title,
            'cat_display': cat_display,
            'date_str': date_str,
            'wordpress_url': draft.get('wordpress_url', ''),
        })

    html = render_template('draft_list.html',
        tab=tab,
        articles=articles,
    )
    return html, 200
