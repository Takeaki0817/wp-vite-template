<?php
/**
 * パフォーマンス最適化（ミニマル）
 *
 * @package ThemeNameHere
 * @since 1.0.0
 */

// 直接アクセスを防止
if (!defined('ABSPATH')) {
  exit();
}

/**
 * ミニマルなパフォーマンス最適化クラス
 */
class ThemePerformance
{
  /**
   * 基本的なパフォーマンス最適化を初期化
   */
  public static function init(): void
  {
    // アセット最適化（基本）
    add_filter(
      'style_loader_src',
      [self::class, 'remove_version_strings'],
      10,
      1
    );
    add_filter(
      'script_loader_src',
      [self::class, 'remove_version_strings'],
      10,
      1
    );

    // キャッシュヘッダー設定
    add_action('wp_loaded', [self::class, 'set_cache_headers']);

    // WordPress絵文字を無効化
    add_action('init', [self::class, 'disable_emojis']);

    // 不要なヘッダー情報を削除
    add_action('init', [self::class, 'clean_wp_head']);
  }

  /**
   * バージョン文字列を削除（セキュリティ向上）
   *
   * @param string $src アセットURL
   * @return string クリーンなURL
   */
  public static function remove_version_strings(string $src): string
  {
    if (strpos($src, 'ver=')) {
      $src = remove_query_arg('ver', $src);
    }
    return $src;
  }

  /**
   * 基本的なキャッシュヘッダーを設定
   */
  public static function set_cache_headers(): void
  {
    if (!is_admin() && !headers_sent()) {
      // 静的ファイルのキャッシュを設定
      header('Cache-Control: public, max-age=31536000'); // 1年
    }
  }

  /**
   * WordPress絵文字機能を無効化
   */
  public static function disable_emojis(): void
  {
    remove_action('wp_head', 'print_emoji_detection_script', 7);
    remove_action('wp_print_styles', 'print_emoji_styles');
    remove_action('admin_print_scripts', 'print_emoji_detection_script');
    remove_action('admin_print_styles', 'print_emoji_styles');
    remove_filter('wp_mail', 'wp_staticize_emoji_for_email');
    remove_filter('the_content_feed', 'wp_staticize_emoji');
    remove_filter('comment_text_rss', 'wp_staticize_emoji');
  }

  /**
   * 不要なWordPressヘッダー情報を削除
   */
  public static function clean_wp_head(): void
  {
    // WordPress バージョン情報を削除
    remove_action('wp_head', 'wp_generator');

    // RSD リンクを削除
    remove_action('wp_head', 'rsd_link');

    // Windows Live Writer 用リンクを削除
    remove_action('wp_head', 'wlwmanifest_link');

    // Shortlink を削除
    remove_action('wp_head', 'wp_shortlink_wp_head');

    // REST API リンクを削除
    remove_action('wp_head', 'rest_output_link_wp_head');
    remove_action('wp_head', 'wp_oembed_add_discovery_links');
  }
}

// 初期化
ThemePerformance::init();
