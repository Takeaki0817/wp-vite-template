<?php
/**
 * テーマのセットアップと設定（ミニマル）
 *
 * @package ThemeNameHere
 * @since 1.0.0
 */

// 直接アクセスを防止
if (!defined('ABSPATH')) {
    exit;
}

/**
 * ミニマルなテーマセットアップと設定
 */
class ThemeSetup
{
    /**
     * キャッシュバスティング用テーマバージョン
     */
    public const THEME_VERSION = '1.0.0';

    /**
     * キャッシュバスティング用の動的バージョンを取得
     */
    private static function get_dynamic_version(): string {
        if (defined('WP_DEBUG') && WP_DEBUG) {
            // 開発環境では現在時刻を使用してキャッシュを無効化
            return time();
        }
        // 本番環境ではstyle.cssの最終更新時刻を使用
        return filemtime(get_template_directory() . '/style.css') ?: self::THEME_VERSION;
    }

    /**
     * テーマを初期化
     */
    public static function init(): void
    {
        add_action('after_setup_theme', [self::class, 'setup_theme_support']);
        add_action('wp_enqueue_scripts', [self::class, 'enqueue_assets']);
        add_filter('script_loader_tag', [self::class, 'add_defer_attribute'], 10, 2);
    }

    /**
     * テーマサポートの設定
     */
    public static function setup_theme_support(): void
    {
        // 動的なタイトルタグのサポート
        add_theme_support('title-tag');

        // アイキャッチ画像の有効化
        add_theme_support('post-thumbnails');

        // HTML5サポート
        add_theme_support('html5', [
            'search-form',
            'comment-form', 
            'comment-list',
            'gallery',
            'caption'
        ]);

        // レスポンシブ埋め込み
        add_theme_support('responsive-embeds');

        // ブロックエディタ用のCSS
        add_theme_support('wp-block-styles');
        add_theme_support('align-wide');

        // カスタムロゴ
        add_theme_support('custom-logo', [
            'height'      => 60,
            'width'       => 200,
            'flex-height' => true,
            'flex-width'  => true,
        ]);

        // カスタム背景
        add_theme_support('custom-background', [
            'default-color' => 'ffffff',
        ]);

        // メニューサポート
        register_nav_menus([
            'primary' => 'プライマリーメニュー',
            'footer'  => 'フッターメニュー',
        ]);
    }

    /**
     * スタイルとスクリプトを読み込み
     */
    public static function enqueue_assets(): void
    {
        $theme_version = self::get_dynamic_version();
        
        // メインスタイルシート
        wp_enqueue_style(
            'theme-style',
            get_template_directory_uri() . '/style.css',
            [],
            $theme_version
        );

        // Tailwind CSS
        if (file_exists(get_template_directory() . '/assets/styles/tailwind.css')) {
            wp_enqueue_style(
                'theme-tailwind',
                get_template_directory_uri() . '/assets/styles/tailwind.css',
                ['theme-style'],
                $theme_version
            );
        }
        
        // 追加スタイル
        if (file_exists(get_template_directory() . '/assets/styles/add-style.css')) {
            wp_enqueue_style(
                'theme-add-style',
                get_template_directory_uri() . '/assets/styles/add-style.css',
                ['theme-tailwind'],
                $theme_version
            );
        }

        // 共通スクリプト
        if (file_exists(get_template_directory() . '/assets/scripts/common.js')) {
            wp_enqueue_script(
                'theme-common',
                get_template_directory_uri() . '/assets/scripts/common.js',
                [],
                $theme_version,
                false
            );
        }
        
        // ページ固有スクリプト
        self::enqueue_page_specific_scripts($theme_version);

        // コメント返信スクリプト
        if (is_singular() && comments_open() && get_option('thread_comments')) {
            wp_enqueue_script('comment-reply');
        }
    }
    
    /**
     * ページ固有スクリプトを読み込み
     *
     * @param string $theme_version テーマバージョン
     */
    private static function enqueue_page_specific_scripts(string $theme_version): void
    {
        $pages_dir = get_template_directory() . '/assets/scripts/pages/';
        
        // /assets/scripts/pages/内のすべてのJSファイルを再帰的に取得
        if (is_dir($pages_dir)) {
            $js_files = self::get_js_files_recursive($pages_dir);
            
            foreach ($js_files as $file_path) {
                // ファイル名からページスラッグを取得
                $relative_path = str_replace($pages_dir, '', $file_path);
                $page_slug = pathinfo($relative_path, PATHINFO_FILENAME);
                $script_handle = 'theme-page-' . sanitize_title($page_slug);
                
                // ページ条件をチェック
                $should_load = false;
                
                if ($page_slug === 'front-page' && is_front_page()) {
                    $should_load = true;
                } elseif (is_page($page_slug)) {
                    $should_load = true;
                } elseif (is_single() && $page_slug === 'single') {
                    $should_load = true;
                } elseif (is_archive() && $page_slug === 'archive') {
                    $should_load = true;
                } elseif (is_404() && $page_slug === '404') {
                    $should_load = true;
                }
                
                // 条件に合致する場合はスクリプトを読み込み
                if ($should_load) {
                    $script_url = get_template_directory_uri() . '/assets/scripts/pages/' . $relative_path;
                    
                    wp_enqueue_script(
                        $script_handle,
                        $script_url,
                        ['theme-common'],
                        $theme_version,
                        false
                    );
                }
            }
        }
    }
    
    /**
     * ディレクトリ内のJSファイルを再帰的に取得
     *
     * @param string $dir ディレクトリパス
     * @return array JSファイルパスの配列
     */
    private static function get_js_files_recursive(string $dir): array
    {
        $js_files = [];
        
        if (!is_dir($dir)) {
            return $js_files;
        }
        
        $iterator = new RecursiveIteratorIterator(
            new RecursiveDirectoryIterator($dir, RecursiveDirectoryIterator::SKIP_DOTS)
        );
        
        foreach ($iterator as $file) {
            if ($file->isFile() && $file->getExtension() === 'js') {
                $js_files[] = $file->getPathname();
            }
        }
        
        return $js_files;
    }
    
    /**
     * スクリプトタグにdefer属性を追加
     *
     * @param string $tag スクリプトタグ
     * @param string $handle スクリプトハンドル
     * @return string 修正されたスクリプトタグ
     */
    public static function add_defer_attribute(string $tag, string $handle): string
    {
        // テーマのスクリプトにのみdefer属性を追加
        if (strpos($handle, 'theme-') === 0) {
            // すでにdefer属性がある場合は重複を避ける
            if (strpos($tag, 'defer') === false) {
                $tag = str_replace(' src', ' defer src', $tag);
            }
        }
        
        return $tag;
    }
}

// 初期化
ThemeSetup::init();