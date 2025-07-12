<?php
/**
 * セキュリティ拡張（ミニマル）
 *
 * @package ThemeNameHere
 * @since 1.0.0
 */

// 直接アクセスを防止
if (!defined('ABSPATH')) {
    exit;
}

/**
 * ミニマルなセキュリティ拡張クラス
 */
class ThemeSecurity
{
    /**
     * 基本的なセキュリティ機能を初期化
     */
    public static function init(): void
    {
        // セキュリティヘッダー
        add_action('send_headers', [self::class, 'send_security_headers']);
        
        // 基本的なWordPress機能の無効化
        add_filter('xmlrpc_enabled', '__return_false');
        add_filter('map_meta_cap', [self::class, 'disable_file_editor'], 10, 2);
        
        // ログインページ保護
        add_filter('login_errors', [self::class, 'generic_login_error']);
        
        // ユーザー列挙攻撃の基本防止
        add_action('wp', [self::class, 'prevent_user_enumeration']);
    }

    /**
     * セキュリティヘッダーを送信
     */
    public static function send_security_headers(): void
    {
        if (!is_admin() && !headers_sent()) {
            header('X-Frame-Options: SAMEORIGIN');
            header('X-Content-Type-Options: nosniff');
            header('X-XSS-Protection: 1; mode=block');
            header('Referrer-Policy: strict-origin-when-cross-origin');
        }
    }

    /**
     * ファイルエディターを無効化
     *
     * @param array $caps 権限配列
     * @param string $cap 権限名
     * @return array 修正された権限配列
     */
    public static function disable_file_editor(array $caps, string $cap): array
    {
        if ($cap === 'edit_plugins' || $cap === 'edit_themes') {
            $caps[] = 'do_not_allow';
        }
        return $caps;
    }

    /**
     * 汎用ログインエラーメッセージ
     *
     * @return string エラーメッセージ
     */
    public static function generic_login_error(): string
    {
        return 'ログインに失敗しました。ユーザー名またはパスワードが正しくありません。';
    }

    /**
     * ユーザー列挙攻撃を防止
     */
    public static function prevent_user_enumeration(): void
    {
        if (!is_user_logged_in() && isset($_GET['author'])) {
            wp_redirect(home_url());
            exit;
        }
    }
}

// 初期化
ThemeSecurity::init();