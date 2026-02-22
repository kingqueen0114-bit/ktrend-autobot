#!/usr/bin/env python3
"""
WordPress に画像クレジット用CSSを追加
カスタムCSSプラグインとして実装
"""

import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()


def create_custom_css_plugin():
    """画像クレジット用のカスタムCSSプラグインを作成"""

    # プラグインのPHPコード
    plugin_code = """<?php
/**
 * Plugin Name: K-TREND TIMES Image Credit Styles
 * Description: 画像クレジット表示用のカスタムCSS
 * Version: 1.0
 * Author: K-TREND TIMES
 */

function ktrend_image_credit_styles() {
    $css = "
    /* K-TREND TIMES 画像クレジットスタイル */
    .image-credit,
    .wp-block-image figcaption.image-credit {
        font-size: 0.75rem;
        color: #666;
        font-style: italic;
        margin-top: 0.5rem;
        text-align: right;
        line-height: 1.4;
    }

    @media (prefers-color-scheme: dark) {
        .image-credit,
        .wp-block-image figcaption.image-credit {
            color: #999;
        }
    }

    @media (max-width: 768px) {
        .image-credit,
        .wp-block-image figcaption.image-credit {
            font-size: 0.7rem;
        }
    }

    .image-credit::before {
        content: '📷 ';
        opacity: 0.7;
    }

    .image-credit a {
        color: inherit;
        text-decoration: none;
        border-bottom: 1px dotted #999;
    }

    .image-credit a:hover {
        border-bottom-style: solid;
        color: #333;
    }
    ";

    echo '<style type="text/css">' . $css . '</style>';
}

add_action('wp_head', 'ktrend_image_credit_styles');
"""

    return plugin_code


def upload_plugin_to_wordpress():
    """プラグインファイルをWordPressにアップロード"""

    wp_url = os.getenv("WORDPRESS_URL", "")
    wp_user = os.getenv("WORDPRESS_USER", "")
    wp_password = os.getenv("WORDPRESS_APP_PASSWORD", "")

    if not all([wp_url, wp_user, wp_password]):
        print("❌ エラー: WordPress設定が見つかりません")
        print("   .envファイルを確認してください")
        return False

    # プラグインコードを生成
    plugin_code = create_custom_css_plugin()

    # ローカルに一時保存
    plugin_path = "ktrend-image-credit-styles.php"
    with open(plugin_path, 'w', encoding='utf-8') as f:
        f.write(plugin_code)

    print("✅ プラグインファイルを生成しました")
    print(f"   ファイル: {plugin_path}")
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📋 次の手順で手動インストールしてください:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    print("1. WordPressサーバーにSSH接続:")
    print("   ssh your-server")
    print()
    print("2. プラグインディレクトリを作成:")
    print("   mkdir -p /var/www/html/wp-content/plugins/ktrend-image-credit-styles")
    print()
    print("3. プラグインファイルをアップロード:")
    print(f"   scp {plugin_path} your-server:/var/www/html/wp-content/plugins/ktrend-image-credit-styles/")
    print()
    print("4. WordPress管理画面でプラグインを有効化:")
    print("   プラグイン → インストール済みプラグイン → 「K-TREND TIMES Image Credit Styles」を有効化")
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    print("または、より簡単な方法:")
    print()
    print("WordPress管理画面 → 外観 → カスタマイズ → 追加CSS")
    print(f"に以下のファイルの内容を貼り付けてください:")
    print()
    print("  wordpress-image-credit-style.css")
    print()

    return True


def main():
    """メイン実行"""
    print("\n" + "=" * 60)
    print("K-TREND TIMES 画像クレジットCSS インストーラー")
    print("=" * 60 + "\n")

    upload_plugin_to_wordpress()

    print("=" * 60)
    print("✅ プラグインファイル生成完了")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
