"""
K-Trend Times 自動修正関数
タスク5: 禁止パターンの自動置換。品質チェック前に実行する。

修正項目:
1. マークダウン強調（**text**）の除去
2. マークダウン斜体（*text*）の除去（クレジット行は保護）
3. 装飾記号（■●▶▷◆◇）の除去
4. 過剰な「!」の削減（記事全体で最大2回まで）
"""

import re
from typing import Dict


def auto_fix_article(article_json: Dict) -> Dict:
    """
    禁止パターンを自動修正して返す。
    元のarticle_jsonは変更せず、修正後のコピーを返す。

    Args:
        article_json: 生成された記事JSON

    Returns:
        修正後の記事JSON（コピー）
    """
    fixed = article_json.copy()
    body = fixed.get("body", "")

    # 1. マークダウン強調（**text**）を除去 → テキストのみにする
    body = re.sub(r'\*\*([^*]+)\*\*', r'\1', body)

    # 2. マークダウン斜体（*text*）を除去（クレジット行は保護）
    lines = body.split('\n')
    fixed_lines = []
    for line in lines:
        if line.strip().startswith('*写真＝') or line.strip().startswith('*Photo'):
            fixed_lines.append(line)  # クレジット行はそのまま
        else:
            fixed_lines.append(re.sub(r'\*([^*]+)\*', r'\1', line))
    body = '\n'.join(fixed_lines)

    # 3. 装飾記号を除去
    body = re.sub(r'[■●▶▷◆◇]\s*', '', body)

    # 4. 過剰な「!」を削減（連続「!」を1つに）
    body = re.sub(r'!{2,}', '!', body)
    # 記事全体で「!」が3回以上あれば、3回目以降を「。」に変換
    excl_positions = [m.start() for m in re.finditer(r'!', body)]
    if len(excl_positions) > 2:
        body_list = list(body)
        for pos in excl_positions[2:]:
            body_list[pos] = '。'
        body = ''.join(body_list)

    fixed["body"] = body
    return fixed
