<?php
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
