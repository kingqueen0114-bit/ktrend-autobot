"""Markdown → Portable Text 変換モジュール

content_generator.py が生成するMarkdownテキストを
Sanity Portable Text JSON配列に変換する。
"""

import re
import uuid
import logging

logger = logging.getLogger(__name__)


def _generate_key():
    """PortableTextブロック用のユニークキーを生成"""
    return uuid.uuid4().hex[:12]


def _parse_inline_marks(text: str):
    """インラインマーク（太字、斜体、リンク）をパースしてspansとmarkDefsを返す"""
    spans = []
    mark_defs = []

    # Combined regex for bold, italic, links
    # Process links first, then bold, then italic
    pattern = re.compile(
        r'\[([^\]]+)\]\(([^)]+)\)'  # [text](url) links
        r'|\*\*(.+?)\*\*'          # **bold**
        r'|\*(.+?)\*'              # *italic*
        r'|([^*\[]+)'              # plain text
    )

    for match in pattern.finditer(text):
        link_text, link_url, bold_text, italic_text, plain_text = match.groups()

        if link_text and link_url:
            key = _generate_key()
            mark_defs.append({
                "_key": key,
                "_type": "link",
                "href": link_url,
            })
            spans.append({
                "_type": "span",
                "_key": _generate_key(),
                "text": link_text,
                "marks": [key],
            })
        elif bold_text:
            spans.append({
                "_type": "span",
                "_key": _generate_key(),
                "text": bold_text,
                "marks": ["strong"],
            })
        elif italic_text:
            spans.append({
                "_type": "span",
                "_key": _generate_key(),
                "text": italic_text,
                "marks": ["em"],
            })
        elif plain_text:
            spans.append({
                "_type": "span",
                "_key": _generate_key(),
                "text": plain_text,
                "marks": [],
            })

    # If no spans were created, return the full text as a single span
    if not spans:
        spans = [{
            "_type": "span",
            "_key": _generate_key(),
            "text": text,
            "marks": [],
        }]

    return spans, mark_defs


def _make_block(text: str, style: str = "normal", list_item: str = None, level: int = 1):
    """テキストからPortable Textブロックを生成"""
    spans, mark_defs = _parse_inline_marks(text)

    block = {
        "_type": "block",
        "_key": _generate_key(),
        "style": style,
        "children": spans,
        "markDefs": mark_defs,
    }

    if list_item:
        block["listItem"] = list_item
        block["level"] = level

    return block


def markdown_to_portable_text(markdown: str) -> list:
    """Markdownテキストを Portable Text JSON配列に変換

    Args:
        markdown: Markdownテキスト

    Returns:
        Portable Text ブロック配列
    """
    if not markdown:
        return []

    blocks = []
    lines = markdown.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Empty line — skip
        if not stripped:
            i += 1
            continue

        # Heading ## or ###
        if stripped.startswith("### "):
            text = stripped[4:].strip()
            blocks.append(_make_block(text, style="h3"))
            i += 1
            continue

        if stripped.startswith("## "):
            text = stripped[3:].strip()
            blocks.append(_make_block(text, style="h2"))
            i += 1
            continue

        if stripped.startswith("# "):
            text = stripped[2:].strip()
            blocks.append(_make_block(text, style="h2"))
            i += 1
            continue

        # Blockquote
        if stripped.startswith("> "):
            text = stripped[2:].strip()
            blocks.append(_make_block(text, style="blockquote"))
            i += 1
            continue

        # Unordered list
        if re.match(r'^[-*+]\s+', stripped):
            text = re.sub(r'^[-*+]\s+', '', stripped)
            blocks.append(_make_block(text, list_item="bullet"))
            i += 1
            continue

        # Ordered list
        if re.match(r'^\d+\.\s+', stripped):
            text = re.sub(r'^\d+\.\s+', '', stripped)
            blocks.append(_make_block(text, list_item="number"))
            i += 1
            continue

        # Image ![alt](url)
        img_match = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)', stripped)
        if img_match:
            alt_text = img_match.group(1)
            img_url = img_match.group(2)
            # Note: Image blocks need an asset reference.
            # For now, create a placeholder — actual asset upload
            # happens in storage_manager before saving to Sanity.
            blocks.append({
                "_type": "image",
                "_key": _generate_key(),
                "_sanity_placeholder_url": img_url,
                "alt": alt_text,
            })
            i += 1
            continue

        # Horizontal rule
        if re.match(r'^---+$', stripped) or re.match(r'^\*\*\*+$', stripped):
            i += 1
            continue

        # Normal paragraph — collect consecutive non-empty lines
        paragraph_lines = [stripped]
        i += 1
        while i < len(lines) and lines[i].strip() and not any([
            lines[i].strip().startswith("#"),
            lines[i].strip().startswith("> "),
            re.match(r'^[-*+]\s+', lines[i].strip()),
            re.match(r'^\d+\.\s+', lines[i].strip()),
            re.match(r'^!\[', lines[i].strip()),
            re.match(r'^---+$', lines[i].strip()),
        ]):
            paragraph_lines.append(lines[i].strip())
            i += 1

        text = " ".join(paragraph_lines)
        blocks.append(_make_block(text))

    return blocks


def body_html_to_portable_text(html_body: str) -> list:
    """HTML本文をPortable Textに変換（フォールバック用）

    主にWordPressからの移行データ用。通常はmarkdown_to_portable_textを使用。
    HTMLをプレーンテキストとして扱い、段落ごとにブロックを生成する。
    """
    if not html_body:
        return []

    # Strip HTML tags for simple conversion
    text = re.sub(r'<br\s*/?>', '\n', html_body)
    text = re.sub(r'</p>', '\n\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = text.strip()

    # Convert each paragraph
    blocks = []
    for para in text.split("\n\n"):
        para = para.strip()
        if para:
            blocks.append(_make_block(para))

    return blocks
