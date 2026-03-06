"""
WordPress 投稿コンテンツ組み立てヘルパー

highlights（チェックポイント）を記事本文に統合し、
AIが生成した Markdown を WordPress 互換 HTML に変換する。

変換内容:
1. highlights → ✔️ CHECKPOINT セクションとして本文上部に挿入
2. Markdown **bold** → <strong>bold</strong>
3. Markdown *italic* → <em>italic</em>（クレジット行のみ）
4. Markdown ## 見出し → <h2>見出し</h2>
5. Markdown ### 見出し → <h3>見出し</h3>
6. URL のテキスト → <a href="URL">URL</a>
"""

import re
from typing import Dict, List, Optional


def build_wp_content(draft_data: Dict) -> str:
    """
    CMS記事データからWordPress投稿用HTMLコンテンツを組み立てる。

    highlights を ✔️ CHECKPOINT セクションとして本文上部に挿入し、
    Markdown マークアップを WordPress 互換 HTML に変換する。

    Args:
        draft_data: CMS記事データ (body, highlights 等)

    Returns:
        WordPress投稿用HTMLコンテンツ
    """
    body = draft_data.get("body", "")
    highlights = draft_data.get("highlights", [])

    # === 1. Markdown → HTML 変換 ===
    body = _convert_markdown_to_html(body)

    # === 2. Highlights（チェックポイント）セクションを構築 ===
    checkpoint_html = _build_checkpoint_html(highlights)

    # === 3. チェックポイントを本文上部に挿入 ===
    if checkpoint_html:
        content = f"{checkpoint_html}\n\n{body}"
    else:
        content = body

    return content


def _build_checkpoint_html(highlights: List[str]) -> str:
    """
    highlights 配列から ✔️ CHECKPOINT HTML を構築する。

    出力例:
    <div class="ktrend-checkpoint">
    <p>✔️ CHECKPOINT</p>
    <ul>
    <li>ハイライト1</li>
    <li>ハイライト2</li>
    <li>ハイライト3</li>
    </ul>
    </div>
    """
    if not highlights:
        return ""

    items = "\n".join(f"<li>{_escape_html(h)}</li>" for h in highlights if h.strip())

    if not items:
        return ""

    return f"""<div class="ktrend-checkpoint">
<p>✔️ CHECKPOINT</p>
<ul>
{items}
</ul>
</div>"""


def _convert_markdown_to_html(text: str) -> str:
    """
    AI生成のMarkdownテキストをWordPress互換HTMLに変換する。

    WordPress のビジュアルエディタでは <strong> / <em> / <h2> 等が
    正しくレンダリングされる。これにより公開記事にアスタリスク等の
    Markdown記号が表示されることを防ぐ。
    """
    lines = text.split("\n")
    html_lines = []

    for line in lines:
        stripped = line.strip()

        # 見出し変換
        if stripped.startswith("### "):
            heading_text = stripped[4:]
            html_lines.append(f"<h3>{heading_text}</h3>")
            continue
        elif stripped.startswith("## "):
            heading_text = stripped[3:]
            html_lines.append(f"<h2>{heading_text}</h2>")
            continue

        # クレジット行は保護（*写真＝...* はそのまま <em> に変換）
        if stripped.startswith("*写真＝") or stripped.startswith("*Photo"):
            # *text* → <em>text</em>
            line = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', line)
            html_lines.append(line)
            continue

        # **太字** → <strong>太字</strong>
        line = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)

        # *斜体* → <em>斜体</em>（残っている場合）
        line = re.sub(r'(?<!\*)\*(?!\*)([^*]+)\*(?!\*)', r'<em>\1</em>', line)

        # URLリンク化: https://... → <a href="...">...</a>
        line = re.sub(
            r'(?<!["\'>])(https?://[^\s<>\)]+)',
            r'<a href="\1" target="_blank" rel="noopener">\1</a>',
            line
        )

        html_lines.append(line)

    return "\n".join(html_lines)


def _escape_html(text: str) -> str:
    """HTMLエスケープ（最低限）"""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
