"""
Draft editor handler for K-Trend AutoBot.
Renders HTML form for viewing and editing drafts, handles POST approval/publishing.
"""
import functions_framework
from datetime import datetime
import json

from src.storage_manager import StorageManager
from utils.logging_config import log_event, log_error


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
            return """
            <html><body style="font-family: sans-serif; text-align: center; padding: 50px;">
            <h1 style="color: #0277bd;">💾 保存完了</h1>
            <p>下書きとして保存しました。LINEの「下書き」メニューから確認できます。</p>
            <a href="https://line.me/R/" style="color: #0277bd; display: inline-block; padding: 15px 30px; border: 1px solid #0277bd; border-radius: 30px; text-decoration: none; margin-top: 20px;">💬 LINEに戻る</a>
            </body></html>
            """, 200

        draft['status'] = 'approved'
        storage.save_draft(draft, draft_id)

        # 4. Publish to WordPress if CMS is approved
        if 'approve_cms' in form:
            # Pass existing WP post ID if available (to update draft → publish)
            wp_post_id = draft.get('wordpress_post_id') or draft.get('wordpress_id')
            result = storage.publish_to_wordpress(cms_content, img_url, category=new_category, artist_tags=artist_tags, wp_post_id=wp_post_id)
            if result:
                draft['wordpress_url'] = result['url']
                draft['wordpress_id'] = result['id']
                storage.save_draft(draft, draft_id)

                # Success page with link
                success_html = f"""
                <!DOCTYPE html>
                <html lang="ja">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>公開完了 - K-Trend</title>
                    <style>
                        body {{ font-family: -apple-system, sans-serif; background: #e8f5e9; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }}
                        .success-card {{ background: white; padding: 40px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); text-align: center; max-width: 500px; }}
                        .success-icon {{ font-size: 64px; margin-bottom: 20px; }}
                        h1 {{ color: #1DB446; margin: 0 0 15px; }}
                        p {{ color: #666; margin: 10px 0; }}
                        .btn {{ display: inline-block; padding: 15px 30px; background: #1DB446; color: white; text-decoration: none; border-radius: 30px; font-weight: bold; margin: 10px 5px; }}
                        .btn-secondary {{ background: #0277bd; }}
                    </style>
                </head>
                <body>
                    <div class="success-card">
                        <div class="success-icon">🎉</div>
                        <h1>公開完了！</h1>
                        <p>記事がWordPressに公開されました。</p>
                        <p style="word-break: break-all; font-size: 14px; color: #888;">{result['url']}</p>
                        <a href="{result['url']}" target="_blank" class="btn">📰 記事を確認</a>
                        <a href="https://line.me/R/" class="btn btn-secondary">💬 LINEに戻る</a>
                    </div>
                </body>
                </html>
                """
                return success_html, 200
            else:
                return """
                <html><body style="font-family: sans-serif; text-align: center; padding: 50px;">
                <h1 style="color: #f44336;">❌ 公開エラー</h1>
                <p>WordPressへの公開に失敗しました。</p>
                <p>しばらく待ってから再度お試しください。</p>
                <a href="javascript:history.back()" style="color: #0277bd;">← 戻る</a>
                </body></html>
                """, 500
        else:
            return """
            <html><body style="font-family: sans-serif; text-align: center; padding: 50px;">
            <h1 style="color: #1DB446;">✅ 保存完了</h1>
            <p>修正内容は保存されました。</p>
            <p style="color: #888;">（CMSにチェックがなかったため、WordPressには公開されていません）</p>
            <a href="javascript:history.back()" style="color: #0277bd;">← 戻る</a>
            </body></html>
            """, 200

    # --- GET Request: Render Form ---

    # Extract content
    sns_content = draft.get('sns_content', {})
    cms_content = draft.get('cms_content', {})
    trend_source = draft.get('trend_source', {})
    category = trend_source.get('category', 'trend')

    # Category display names
    category_names = {
        'artist': 'K-POP・アーティスト',
        'beauty': 'ビューティー',
        'fashion': 'ファッション',
        'food': 'グルメ',
        'travel': '韓国旅行',
        'event': 'イベント',
        'drama': 'ドラマ',
        'trend': 'トレンド',
        'other': 'その他'
    }
    category_display = category_names.get(category, 'トレンド')

    # Escape content for JavaScript
    import html as html_module
    title_escaped = html_module.escape(cms_content.get('title', ''))
    body_escaped = html_module.escape(cms_content.get('body', ''))
    meta_escaped = html_module.escape(cms_content.get('meta_description', ''))

    # Generate HTML with enhanced editor
    html = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>K-Trend 編集・承認</title>
        <!-- Use reliable CDN for marked.js -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.0/marked.min.js"></script>
        <style>
            * {{ box-sizing: border-box; }}
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 0; background: #f0f2f5; }}

            /* Tab Navigation */
            .tab-nav {{ display: flex; background: #1DB446; position: sticky; top: 0; z-index: 100; }}
            .tab-btn {{ flex: 1; padding: 15px; border: none; background: transparent; color: white; font-size: 16px; font-weight: bold; cursor: pointer; transition: background 0.3s; }}
            .tab-btn:hover {{ background: rgba(255,255,255,0.1); }}
            .tab-btn.active {{ background: rgba(255,255,255,0.2); border-bottom: 3px solid white; }}

            .tab-content {{ display: none; }}
            .tab-content.active {{ display: block; }}

            /* Editor Panel */
            .editor-panel {{ max-width: 900px; margin: 0 auto; padding: 20px; }}
            .editor-container {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }}

            h2 {{ color: #1DB446; margin-top: 0; padding-bottom: 10px; border-bottom: 2px solid #e8f5e9; }}
            h3 {{ color: #333; margin: 20px 0 10px; }}

            label {{ font-weight: 600; display: block; margin-bottom: 8px; color: #333; }}
            input[type="text"], input[type="url"], textarea, select {{
                width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px;
                font-size: 15px; transition: border-color 0.3s; background: white;
            }}
            input:focus, textarea:focus, select:focus {{ border-color: #1DB446; outline: none; }}
            textarea {{ min-height: 120px; resize: vertical; line-height: 1.6; }}
            select {{ cursor: pointer; }}
            .tag-input-hint {{ color: #888; font-size: 12px; margin-top: 5px; }}
            .tag-preview {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }}
            .tag-badge {{ background: #e3f2fd; color: #1976d2; padding: 5px 12px; border-radius: 15px; font-size: 13px; display: inline-flex; align-items: center; }}
            .tag-badge:before {{ content: '#'; margin-right: 2px; }}

            .image-section {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
            .image-preview {{ max-width: 100%; max-height: 300px; border-radius: 8px; margin: 10px 0; object-fit: cover; }}
            .image-input-group {{ display: flex; gap: 10px; margin-top: 10px; }}
            .image-input-group input {{ flex: 1; }}
            .btn-update-image {{ padding: 12px 20px; background: #0277bd; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }}
            .btn-update-image:hover {{ background: #01579b; }}

            .checkbox-row {{ display: flex; align-items: center; gap: 10px; padding: 12px; background: #fff8e1; border-radius: 8px; margin-bottom: 15px; }}
            .checkbox-row input[type="checkbox"] {{ width: 20px; height: 20px; }}

            .submit-section {{ position: sticky; bottom: 0; background: white; padding: 20px; border-top: 1px solid #eee; margin: 0 -25px -25px; border-radius: 0 0 12px 12px; }}
            .submit-btn {{ width: 100%; padding: 18px; background: #1DB446; color: white; border: none; border-radius: 30px; font-size: 18px; font-weight: bold; cursor: pointer; }}
            .submit-btn:hover {{ background: #159e3c; }}

            /* Preview Panel - K-TREND TIMES Style */
            .preview-panel {{ background: white; min-height: 100vh; }}
            .site-header {{ background: linear-gradient(135deg, #1DB446 0%, #0d7a2e 100%); padding: 15px 20px; text-align: center; }}
            .site-logo {{ color: white; font-size: 24px; font-weight: bold; margin: 0; }}
            .site-logo span {{ color: #ffd700; }}

            .article-container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
            .article-category {{ display: inline-block; background: #1DB446; color: white; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; margin-bottom: 15px; }}
            .article-title {{ font-size: 28px; font-weight: bold; color: #222; line-height: 1.4; margin-bottom: 20px; }}
            .article-meta {{ color: #888; font-size: 14px; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #eee; }}
            .article-featured-image {{ width: 100%; max-height: 450px; object-fit: cover; border-radius: 12px; margin-bottom: 25px; }}
            .article-body {{ font-size: 16px; line-height: 1.9; color: #333; }}
            .article-body h2 {{ font-size: 22px; color: #1DB446; margin: 30px 0 15px; padding-left: 15px; border-left: 4px solid #1DB446; }}
            .article-body h3 {{ font-size: 18px; color: #333; margin: 25px 0 10px; }}
            .article-body p {{ margin-bottom: 20px; }}
            .article-body ul, .article-body ol {{ margin: 15px 0; padding-left: 25px; }}
            .article-body li {{ margin-bottom: 8px; }}
            .article-body blockquote {{ background: #f8f9fa; border-left: 4px solid #1DB446; padding: 15px 20px; margin: 20px 0; font-style: italic; }}

            .meta-preview {{ background: #f0f7f1; padding: 15px; border-radius: 8px; margin-top: 30px; }}
            .meta-preview-title {{ font-weight: bold; color: #1DB446; margin-bottom: 10px; }}
            .meta-preview-text {{ color: #666; font-size: 14px; }}

            /* Mobile */
            @media (max-width: 768px) {{
                .article-title {{ font-size: 22px; }}
                .article-body {{ font-size: 15px; }}
            }}
        </style>
    </head>
    <body>
        <!-- Tab Navigation -->
        <div class="tab-nav">
            <button class="tab-btn active" onclick="showTab('edit')">✏️ 編集</button>
            <button class="tab-btn" onclick="showTab('preview')">👁️ プレビュー</button>
        </div>

        <!-- Edit Tab -->
        <div id="tab-edit" class="tab-content active">
            <div class="editor-panel">
                <form method="POST" id="editForm" enctype="multipart/form-data">

                    <!-- Image Section -->
                    <div class="editor-container">
                        <h2>🖼️ アイキャッチ画像</h2>
                        <div class="image-section">
                            <img id="preview-image" src="{trend_source.get('image_url', '')}" class="image-preview"
                                 onerror="this.src='https://via.placeholder.com/800x450?text=画像を設定してください'">
                            <label style="margin-top: 15px;">📷 画像クレジット・出典</label>
                            <input type="text" id="image_source" name="image_source" 
                                   value="{trend_source.get('image_source', '')}" 
                                   placeholder="例: Photo by Unsplash, BigHit Music提供"
                                   style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px;">
                            <p style="color: #888; font-size: 12px; margin-top: 5px;">※ 画像の出典やクレジットを入力してください。記事に表示されます。</p>

                            <label style="margin-top: 15px;">📁 画像ファイルをアップロード</label>
                            <input type="file" id="image_file" name="image_file" accept="image/*"
                                   style="width: 100%; padding: 10px; border: 2px dashed #ccc; border-radius: 8px; background: #fafafa; cursor: pointer;"
                                   onchange="previewUploadedImage(this)">
                            <p style="color: #888; font-size: 12px; margin-top: 5px;">※ JPG, PNG, WebP対応（最大10MB）</p>

                            <label style="margin-top: 15px;">🔗 または画像URL（変更する場合は新しいURLを入力）</label>
                            <div class="image-input-group">
                                <input type="url" id="image_url" name="image_url" value="{trend_source.get('image_url', '')}" placeholder="https://example.com/image.jpg">
                                <button type="button" class="btn-update-image" onclick="updateImagePreview()">プレビュー更新</button>
                            </div>
                            <p style="color: #888; font-size: 12px; margin-top: 8px;">※ ファイルアップロード優先。URLはファイル未選択時に使用されます</p>
                        </div>
                    </div>

                    <!-- Category & Tags Section -->
                    <div class="editor-container">
                        <h2>🏷️ カテゴリー・タグ</h2>

                        <label>カテゴリー</label>
                        <select id="category" name="category" onchange="updateCategoryPreview()">
                            <option value="artist" {"selected" if category == "artist" else ""}>🎤 K-POP・アーティスト</option>
                            <option value="beauty" {"selected" if category == "beauty" else ""}>💄 ビューティー</option>
                            <option value="fashion" {"selected" if category == "fashion" else ""}>👗 ファッション</option>
                            <option value="food" {"selected" if category == "food" else ""}>🍜 グルメ</option>
                            <option value="travel" {"selected" if category == "travel" else ""}>✈️ 韓国旅行</option>
                            <option value="event" {"selected" if category == "event" else ""}>🎪 イベント</option>
                            <option value="drama" {"selected" if category == "drama" else ""}>📺 ドラマ</option>
                            <option value="trend" {"selected" if category == "trend" else ""}>📈 トレンド</option>
                            <option value="other" {"selected" if category == "other" else ""}>📰 その他</option>
                        </select>

                        <label style="margin-top: 20px;">アーティストタグ（カンマ区切り）</label>
                        <input type="text" id="artist_tags" name="artist_tags"
                               value="{', '.join(trend_source.get('artist_tags', []))}"
                               placeholder="例: BTS, BLACKPINK, NewJeans"
                               oninput="updateTagPreview()">
                        <p class="tag-input-hint">複数のタグはカンマ（,）で区切ってください。WordPressのタグとして登録されます。</p>
                        <div id="tag-preview" class="tag-preview"></div>
                    </div>

                    <!-- Article Content -->
                    <div class="editor-container">
                        <h2>📝 記事コンテンツ</h2>

                        <div class="checkbox-row">
                            <input type="checkbox" id="approve_cms" name="approve_cms" checked>
                            <label for="approve_cms" style="margin: 0; cursor: pointer;">この記事をWordPressに公開する</label>
                        </div>

                        <label>タイトル</label>
                        <input type="text" id="cms_title" name="cms_title" value="{title_escaped}" oninput="updatePreview()">

                        <h3>メタ説明（SEO用・160文字以内推奨）</h3>
                        <textarea id="cms_meta" name="cms_meta" style="height: 80px;" oninput="updatePreview()">{meta_escaped}</textarea>
                        <p style="color: #888; font-size: 12px; text-align: right;"><span id="meta-count">0</span>/160文字</p>

                        <h3>本文（Markdown形式）</h3>
                        <!-- Hidden file input for inline image upload -->
                        <input type="file" id="inline-image-upload" accept="image/*" style="display: none;" onchange="uploadInlineImage(this)">
                        
                        <div style="display: flex; gap: 8px; margin-bottom: 8px; flex-wrap: wrap;">
                            <button type="button" onclick="document.getElementById('inline-image-upload').click()" style="padding: 8px 16px; background: #0277bd; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px;">📷 画像を追加</button>
                            <button type="button" onclick="insertMarkdown('## ')" style="padding: 8px 12px; background: #e0e0e0; border: none; border-radius: 6px; cursor: pointer; font-size: 13px;">H2</button>
                            <button type="button" onclick="insertMarkdown('### ')" style="padding: 8px 12px; background: #e0e0e0; border: none; border-radius: 6px; cursor: pointer; font-size: 13px;">H3</button>
                            <button type="button" onclick="wrapSelection('**')" style="padding: 8px 12px; background: #e0e0e0; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: bold;">B</button>
                            <button type="button" onclick="insertMarkdown('&gt; ')" style="padding: 8px 12px; background: #e0e0e0; border: none; border-radius: 6px; cursor: pointer; font-size: 13px;">引用</button>
                            <button type="button" onclick="insertMarkdown('- ')" style="padding: 8px 12px; background: #e0e0e0; border: none; border-radius: 6px; cursor: pointer; font-size: 13px;">リスト</button>
                        </div>
                        <textarea id="cms_body" name="cms_body" style="height: 400px;" oninput="updatePreview()">{body_escaped}</textarea>
                        <p style="color: #888; font-size: 12px;">Markdownが使えます: **太字**, ## 見出し, - リスト, > 引用, ![説明](URL) 画像</p>
                    </div>

                    <!-- X Posts -->
                    <div class="editor-container">
                        <h2>🐦 X (Twitter) 投稿案</h2>

                        <label>投稿案 1</label>
                        <textarea name="x_post_1" style="height: 100px;">{cms_content.get('x_post_1', '')}</textarea>

                        <label style="margin-top: 20px;">投稿案 2</label>
                        <textarea name="x_post_2" style="height: 100px;">{cms_content.get('x_post_2', '')}</textarea>
                    </div>

                    <!-- SNS Section (Collapsed) -->
                    <details class="editor-container">
                        <summary style="cursor: pointer; font-weight: bold; color: #1DB446;">📱 SNS投稿バリエーション（クリックで展開）</summary>
                        <div style="margin-top: 15px;">
                            <div class="checkbox-row">
                                <input type="checkbox" id="approve_news" name="approve_news" checked>
                                <label for="approve_news" style="margin: 0;">ニュース投稿</label>
                            </div>
                            <textarea name="news_post">{sns_content.get('news_post', '')}</textarea>

                            <div class="checkbox-row" style="margin-top: 15px;">
                                <input type="checkbox" id="approve_luna_a" name="approve_luna_a" checked>
                                <label for="approve_luna_a" style="margin: 0;">Luna投稿A</label>
                            </div>
                            <textarea name="luna_post_a">{sns_content.get('luna_post_a', '')}</textarea>

                            <div class="checkbox-row" style="margin-top: 15px;">
                                <input type="checkbox" id="approve_luna_b" name="approve_luna_b" checked>
                                <label for="approve_luna_b" style="margin: 0;">Luna投稿B</label>
                            </div>
                            <textarea name="luna_post_b">{sns_content.get('luna_post_b', '')}</textarea>
                        </div>
                    </details>

                    <!-- Submit -->
                    <div class="submit-section">
                        <button type="submit" class="submit-btn" name="action_type" value="publish">✅ WordPressに公開する</button>
                        <button type="submit" class="submit-btn" style="background: #0277bd; margin-top: 10px;" name="action_type" value="save_draft">💾 下書きとして保存する</button>
                        <p style="text-align: center; color: #888; font-size: 13px; margin: 10px 0 0;">チェックした項目のみ公開・保存されます</p>
                    </div>
                </form>
            </div>
        </div>

        <!-- Preview Tab -->
        <div id="tab-preview" class="tab-content">
            <div class="preview-panel">
                <!-- Site Header Mock -->
                <div class="site-header">
                    <h1 class="site-logo">K-TREND <span>TIMES</span></h1>
                </div>

                <div class="article-container">
                    <span id="preview-category" class="article-category">{category_display}</span>
                    <h1 id="preview-title" class="article-title">{title_escaped}</h1>
                    <div class="article-meta">
                        <span>📅 {datetime.now().strftime('%Y年%m月%d日')}</span> ·
                        <span>🏷️ <span id="preview-category-meta">{category_display}</span></span>
                    </div>
                    <img id="preview-featured-image" class="article-featured-image" src="{trend_source.get('image_url', '')}"
                         onerror="this.src='https://via.placeholder.com/800x450?text=No+Image'">
                    <div id="preview-body" class="article-body"></div>

                    <div class="meta-preview">
                        <div class="meta-preview-title">📋 メタ説明（検索結果に表示されます）</div>
                        <div id="preview-meta" class="meta-preview-text">{meta_escaped}</div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            // Tab switching
            function showTab(tabName) {{
                document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
                document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
                document.getElementById('tab-' + tabName).classList.add('active');
                const btn = document.querySelector(`button[onclick=\"showTab('${{tabName}}')\"]`);
                if (btn) btn.classList.add('active');
                if (tabName === 'preview') updatePreview();
            }}

            // Update image preview
            function updateImagePreview() {{
                const url = document.getElementById('image_url').value;
                document.getElementById('preview-image').src = url;
                document.getElementById('preview-featured-image').src = url;
            }}

            // Category display names
            const categoryNames = {{
                'artist': '🎤 K-POP・アーティスト',
                'beauty': '💄 ビューティー',
                'fashion': '👗 ファッション',
                'food': '🍜 グルメ',
                'travel': '✈️ 韓国旅行',
                'event': '🎪 イベント',
                'drama': '📺 ドラマ',
                'trend': '📈 トレンド',
                'other': '📰 その他'
            }};

            // Update category preview
            function updateCategoryPreview() {{
                const category = document.getElementById('category').value;
                const displayName = categoryNames[category] || 'トレンド';
                document.getElementById('preview-category').textContent = displayName;
                document.getElementById('preview-category-meta').textContent = displayName;
            }}

            // Update tag preview
            function updateTagPreview() {{
                const tagsInput = document.getElementById('artist_tags').value;
                const tags = tagsInput.split(',').map(t => t.trim()).filter(t => t);
                const container = document.getElementById('tag-preview');
                container.innerHTML = tags.map(tag => `<span class="tag-badge">${{tag}}</span>`).join('');
            }}

            // Update preview content
            function updatePreview() {{
                const title = document.getElementById('cms_title').value;
                const body = document.getElementById('cms_body').value;
                const meta = document.getElementById('cms_meta').value;

                document.getElementById('preview-title').textContent = title;
                document.getElementById('preview-meta').textContent = meta;
                document.getElementById('meta-count').textContent = meta.length;

                // Update category in preview
                updateCategoryPreview();

                // Parse Markdown
                if (typeof marked !== 'undefined') {{
                    document.getElementById('preview-body').innerHTML = marked.parse(body);
                }} else {{
                    document.getElementById('preview-body').innerHTML = body.replace(/\\n/g, '<br>');
                }}
            }}

            // Initial preview update
            document.addEventListener('DOMContentLoaded', function() {{
                updatePreview();
                updateTagPreview();
            }});

            // Preview uploaded file
            let objectUrl = null;
            function previewUploadedImage(input) {{
                if (input.files && input.files[0]) {{
                    if (objectUrl) {{
                        URL.revokeObjectURL(objectUrl);
                    }}
                    objectUrl = URL.createObjectURL(input.files[0]);
                    document.getElementById('preview-image').src = objectUrl;
                    document.getElementById('preview-featured-image').src = objectUrl;
                }}
            }}

            // Upload inline image and insert markdown
            function uploadInlineImage(input) {{
                if (!input.files || !input.files[0]) return;

                const file = input.files[0];
                const formData = new FormData();
                formData.append('action', 'upload_image');
                formData.append('file', file);
                
                // Show loading state
                const btn = document.querySelector('button[onclick*="inline-image-upload"]');
                const originalText = btn.textContent;
                btn.textContent = "⏳ アップロード中...";
                btn.disabled = true;

                fetch(window.location.href, {{
                    method: 'POST',
                    body: formData
                }})
                .then(response => response.json())
                .then(data => {{
                    if (data.url) {{
                        const markdown = `\\n![画像](${{data.url}})\\n`;
                        insertAtCursor('cms_body', markdown);
                        updatePreview();
                    }} else {{
                        alert('アップロード失敗: ' + (data.error || '不明なエラー'));
                    }}
                }})
                .catch(error => {{
                    console.error('Error:', error);
                    alert('アップロードエラーが発生しました');
                }})
                .finally(() => {{
                    btn.textContent = originalText;
                    btn.disabled = false;
                    input.value = ''; // Reset input
                }});
            }}

            // (Legacy) Insert inline image by URL
            function insertInlineImage() {{
                const imageUrl = prompt('画像URLを入力してください:', 'https://');
                if (!imageUrl || imageUrl === 'https://') return;
                const altText = prompt('画像の説明（alt属性）:', '') || '画像';
                const markdown = '\\n![' + altText + '](' + imageUrl + ')\\n';
                insertAtCursor('cms_body', markdown);
            }}

            // Insert markdown at cursor position
            function insertMarkdown(prefix) {{
                const textarea = document.getElementById('cms_body');
                const start = textarea.selectionStart;
                const end = textarea.selectionEnd;
                const text = textarea.value;
                
                // Find the start of the current line
                const lineStart = text.lastIndexOf('\\n', start - 1) + 1;
                textarea.value = text.substring(0, lineStart) + prefix + text.substring(lineStart);
                textarea.selectionStart = textarea.selectionEnd = start + prefix.length;
                textarea.focus();
                updatePreview();
            }}

            // Wrap selection with markdown (e.g. bold)
            function wrapSelection(wrapper) {{
                const textarea = document.getElementById('cms_body');
                const start = textarea.selectionStart;
                const end = textarea.selectionEnd;
                const text = textarea.value;
                const selected = text.substring(start, end) || '文字';
                textarea.value = text.substring(0, start) + wrapper + selected + wrapper + text.substring(end);
                textarea.selectionStart = start + wrapper.length;
                textarea.selectionEnd = start + wrapper.length + selected.length;
                textarea.focus();
                updatePreview();
            }}

            // Insert text at cursor position
            function insertAtCursor(textareaId, text) {{
                const textarea = document.getElementById(textareaId);
                const start = textarea.selectionStart;
                const end = textarea.selectionEnd;
                textarea.value = textarea.value.substring(0, start) + text + textarea.value.substring(end);
                textarea.selectionStart = textarea.selectionEnd = start + text.length;
                textarea.focus();
                updatePreview();
            }}
        </script>
    </body>
    </html>
    """

    return html, 200

def view_article_list(request):
    """
    HTTP endpoint to display a list of drafts and published articles.
    URL: /drafts?tab=pending (default) or /drafts?tab=published
    """
    tab = request.args.get('tab', 'pending')
    storage = StorageManager()
    from google.cloud.firestore_v1.base_query import FieldFilter
    
    # Query logic based on tab
    if tab == 'pending':
        query = storage.db.collection(storage.collection_name).where(filter=FieldFilter('status', 'in', ['draft', 'pending']))
    elif tab == 'published':
        query = storage.db.collection(storage.collection_name).where(filter=FieldFilter('status', 'in', ['approved', 'published']))
    else:
        query = storage.db.collection(storage.collection_name).where(filter=FieldFilter('status', 'in', ['draft', 'pending']))
    
    # Sort and execute
    query = query.order_by('created_at', direction='DESCENDING').limit(50)
    docs = list(query.stream())
    
    articles_html = ""
    if not docs:
        articles_html = f'<div class="empty-state"><h3>記事が見つかりません</h3><p>現在、{ "未公開" if tab == "pending" else "公開済み" }の記事はありません。</p></div>'
    else:
        for doc in docs:
            draft = doc.to_dict()
            draft_id = doc.id
            cms_content = draft.get('cms_content', {})
            title = cms_content.get('title', '無題')
            trend_source = draft.get('trend_source', {})
            category = trend_source.get('category', 'trend')
            status = draft.get('status', 'unknown')
            
            created_at = draft.get('created_at')
            date_str = ""
            if created_at:
                try:
                    date_str = created_at.strftime("%Y-%m-%d %H:%M")
                except:
                    date_str = str(created_at)

            # Category labels
            category_names = {
                'artist': 'K-POP', 'beauty': '美容', 'fashion': '服',
                'food': 'グルメ', 'travel': '旅行', 'event': 'イベント',
                'drama': 'ドラマ', 'trend': 'トレンド', 'other': 'その他'
            }
            cat_display = category_names.get(category, 'トレンド')
            
            # WP Link
            wp_link = ""
            if tab == 'published' and draft.get('wordpress_url'):
                wp_link = f'<a href="{draft.get("wordpress_url")}" target="_blank" class="wp-link">🔗 記事を見る</a>'

            articles_html += f'''
            <div class="article-card">
                <div class="article-meta">
                    <span class="category-badge">{cat_display}</span>
                    <span class="date">{date_str}</span>
                </div>
                <h3 class="article-title">{title}</h3>
                <div class="article-actions">
                    <a href="/draft/{draft_id}" class="btn-edit">✏️ 編集</a>
                    {wp_link}
                </div>
            </div>
            '''
    
    html = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>記事管理一覧 - K-Trend</title>
        <style>
            * {{ box-sizing: border-box; }}
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 0; background: #f0f2f5; }}
            .header {{ background: linear-gradient(135deg, #1DB446 0%, #0d7a2e 100%); padding: 20px; color: white; text-align: center; }}
            .header h1 {{ margin: 0; font-size: 22px; }}
            
            .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
            
            .tabs {{ display: flex; background: white; border-radius: 8px; overflow: hidden; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
            .tab {{ flex: 1; text-align: center; padding: 15px; text-decoration: none; color: #666; font-weight: bold; border-bottom: 3px solid transparent; transition: all 0.3s; }}
            .tab:hover {{ background: #f9f9f9; }}
            .tab.active {{ color: #1DB446; border-bottom: 3px solid #1DB446; background: #e8f5e9; }}
            
            .article-card {{ background: white; padding: 20px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); transition: transform 0.2s; }}
            .article-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
            
            .article-meta {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
            .category-badge {{ background: #e3f2fd; color: #1976d2; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }}
            .date {{ color: #888; font-size: 13px; }}
            
            .article-title {{ margin: 0 0 15px 0; color: #333; font-size: 18px; line-height: 1.4; }}
            
            .article-actions {{ display: flex; gap: 10px; }}
            .btn-edit {{ display: inline-block; padding: 10px 20px; background: #1DB446; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 14px; text-align: center; flex: 1; }}
            .btn-edit:hover {{ background: #159e3c; }}
            .wp-link {{ display: inline-block; padding: 10px 20px; background: #f0f2f5; color: #333; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 14px; text-align: center; flex: 1; }}
            .wp-link:hover {{ background: #e4e6e9; }}
            
            .empty-state {{ background: white; padding: 40px 20px; border-radius: 12px; text-align: center; color: #666; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📋 記事管理一覧</h1>
        </div>
        
        <div class="container">
            <div class="tabs">
                <a href="/drafts?tab=pending" class="tab {'active' if tab == 'pending' else ''}">未公開記事（下書き）</a>
                <a href="/drafts?tab=published" class="tab {'active' if tab == 'published' else ''}">公開済み記事</a>
            </div>
            
            <div class="article-list">
                {articles_html}
            </div>
        </div>
    </body>
    </html>
    """
    return html, 200
