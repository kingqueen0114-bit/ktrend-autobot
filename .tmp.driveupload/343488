<?php
require_once("/var/www/html/wp-load.php");

global $wpdb;

// Find posts with URL-encoded blockquote content
$posts = $wpdb->get_results("
    SELECT ID, post_content
    FROM {$wpdb->posts}
    WHERE post_content LIKE '%blockquote%3C%'
       OR post_content LIKE '%3Cblockquote%'
       OR post_content LIKE '%25blockquote%'
");

echo "Found " . count($posts) . " posts to fix\n";

foreach ($posts as $post) {
    $content = $post->post_content;

    // Decode URL-encoded content
    $decoded = urldecode($content);

    // If still encoded, decode again (double encoding)
    if (strpos($decoded, "%3C") !== false || strpos($decoded, "%22") !== false) {
        $decoded = urldecode($decoded);
    }

    if ($decoded !== $content) {
        $wpdb->update(
            $wpdb->posts,
            array("post_content" => $decoded),
            array("ID" => $post->ID)
        );
        echo "Fixed post ID: " . $post->ID . "\n";
    }
}

// Clear cache
wp_cache_flush();

echo "Done!\n";
