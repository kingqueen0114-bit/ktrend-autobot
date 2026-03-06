
            // Tab switching
            function showTab(tabName) {{
                document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
                document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
                document.getElementById('tab-' + tabName).classList.add('active');
                event.target.classList.add('active');
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
            function previewUploadedImage(input) {{
                if (input.files && input.files[0]) {{
                    const reader = new FileReader();
                    reader.onload = function(e) {{
                        document.getElementById('preview-image').src = e.target.result;
                        document.getElementById('preview-featured-image').src = e.target.result;
                    }};
                    reader.readAsDataURL(input.files[0]);
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
        