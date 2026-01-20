<?php
/**
 * メディア・画像最適化（セーフモード）
 *
 * @package WpViteTheme
 * @since 1.0.0
 */

// 直接アクセスを防止
if (!defined('ABSPATH')) {
    exit;
}

/**
 * 安全なメディア最適化クラス
 * 軽量で安全な画像最適化機能のみ実装
 */
class ThemeMediaOptimization
{
    /**
     * メディア最適化を初期化（セーフモード）
     */
    public static function init(): void
    {
        // 安全な基本設定のみ
        add_action('after_setup_theme', [self::class, 'setup_basic_image_support']);
        
        // 軽量な画像品質設定
        add_filter('jpeg_quality', [self::class, 'set_jpeg_quality']);
        add_filter('wp_editor_set_quality', [self::class, 'set_jpeg_quality']);
        
        // 基本的な遅延読み込み（安全）
        add_filter('wp_get_attachment_image_attributes', [self::class, 'add_safe_lazy_loading'], 10, 3);
        
        // ファイル名の基本最適化
        add_filter('sanitize_file_name', [self::class, 'safe_optimize_filename'], 10);
        
        // SVGサポート（管理者のみ、安全）
        if (current_user_can('manage_options')) {
            add_filter('upload_mimes', [self::class, 'add_svg_support']);
        }
        
        // 大きな画像のしきい値を緩和（WordPressデフォルトの圧縮を軽減）
        add_filter('big_image_size_threshold', [self::class, 'increase_big_image_threshold']);
        
        // アップロード制限を解除
        add_filter('wp_max_upload_size', [self::class, 'increase_upload_limit']);
        
        // WebP変換機能を追加（パレット画像対応済み）
        add_filter('wp_handle_upload', [self::class, 'convert_to_webp']);
        
        // 画像圧縮機能を追加
        add_filter('wp_generate_attachment_metadata', [self::class, 'compress_image'], 10, 2);
        
        // WebPファイルタイプサポート
        add_filter('upload_mimes', [self::class, 'add_webp_support']);
        
        // 管理画面でのメディア処理時のリソース確保
        if (is_admin()) {
            add_action('admin_init', [self::class, 'ensure_media_resources']);
        }
    }
    
    /**
     * 基本的な画像サポートを設定
     */
    public static function setup_basic_image_support(): void
    {
        // レスポンシブ画像を有効化
        add_theme_support('responsive-embeds');
        
        // 基本的なカスタム画像サイズ
        add_image_size('hero', 1920, 1080, true);
        add_image_size('card', 600, 400, true);
        add_image_size('square', 400, 400, true);
    }

    /**
     * JPEG品質を設定（控えめ）
     *
     * @return int 品質値
     */
    public static function set_jpeg_quality(): int
    {
        return 90; // 高品質を維持（WordPressデフォルト82より高い）
    }

    /**
     * 安全な遅延読み込み属性を追加
     *
     * @param array $attr 画像属性
     * @param WP_Post $attachment 添付ファイル
     * @param string $size 画像サイズ
     * @return array 修正された属性
     */
    public static function add_safe_lazy_loading(array $attr, WP_Post $attachment = null, string $size = ''): array
    {
        // 最初の画像は即座に読み込む（LCP最適化）
        static $first_image = true;
        
        if ($first_image && (is_single() || is_page())) {
            $first_image = false;
            $attr['loading'] = 'eager';
            $attr['fetchpriority'] = 'high';
        } else {
            $attr['loading'] = 'lazy';
            $attr['decoding'] = 'async';
        }
        
        return $attr;
    }

    /**
     * SVGサポートを追加（安全版）
     *
     * @param array $mimes MIMEタイプ配列
     * @return array 修正されたMIMEタイプ配列
     */
    public static function add_svg_support(array $mimes): array
    {
        // 管理者のみSVGアップロードを許可
        if (current_user_can('manage_options')) {
            $mimes['svg'] = 'image/svg+xml';
        }
        
        return $mimes;
    }

    /**
     * ファイル名を安全に最適化
     *
     * @param string $filename ファイル名
     * @return string 最適化されたファイル名
     */
    public static function safe_optimize_filename(string $filename): string
    {
        // 基本的な文字変換のみ（安全）
        $filename = mb_convert_kana($filename, 'a', 'UTF-8');
        $filename = sanitize_title($filename);
        
        return $filename;
    }
    
    /**
     * 大きな画像のしきい値を増加（WordPressの自動圧縮を軽減）
     *
     * @return int しきい値（ピクセル）
     */
    public static function increase_big_image_threshold(): int
    {
        // WordPressデフォルト2560pxから4096pxに変更
        return 4096;
    }
    
    /**
     * アップロード制限を解除（サイズ制限なし）
     *
     * @return int アップロードサイズ制限（バイト）
     */
    public static function increase_upload_limit(): int
    {
        // 500MB制限（実質無制限）
        return 500 * 1024 * 1024;
    }
    
    /**
     * メディア処理用リソースを確保
     */
    public static function ensure_media_resources(): void
    {
        // メモリ制限を一時的に増加（管理画面のみ）
        if (is_admin() && !wp_doing_ajax()) {
            $current_memory = ini_get('memory_limit');
            $memory_in_bytes = wp_convert_hr_to_bytes($current_memory);
            $min_memory = 512 * 1024 * 1024; // 512MB
            
            if ($memory_in_bytes < $min_memory) {
                @ini_set('memory_limit', '512M');
            }
            
            // 実行時間制限を調整
            if (!ini_get('safe_mode')) {
                @set_time_limit(300); // 5分
            }
        }
    }
    
    /**
     * WebPサポートを追加
     *
     * @param array $mimes MIMEタイプ配列
     * @return array 修正されたMIMEタイプ配列
     */
    public static function add_webp_support(array $mimes): array
    {
        $mimes['webp'] = 'image/webp';
        return $mimes;
    }
    
    /**
     * アップロード時にWebP形式に変換
     *
     * @param array $upload アップロード情報
     * @return array 処理済みアップロード情報
     */
    public static function convert_to_webp(array $upload): array
    {
        // エラーがある場合はそのまま返す
        if (isset($upload['error']) && $upload['error'] !== false) {
            return $upload;
        }
        
        $file_path = $upload['file'];
        $file_type = $upload['type'];
        
        // 画像ファイルかチェック
        if (strpos($file_type, 'image/') !== 0) {
            return $upload;
        }
        
        // WebPがサポートされているかチェック
        if (!function_exists('imagewebp')) {
            return $upload;
        }
        
        // すでにWebPファイルの場合はそのまま
        if ($file_type === 'image/webp') {
            return $upload;
        }
        
        try {
            $image = null;
            
            // 元画像を読み込み
            switch ($file_type) {
                case 'image/jpeg':
                    $image = imagecreatefromjpeg($file_path);
                    break;
                case 'image/png':
                    $image = imagecreatefrompng($file_path);
                    break;
                case 'image/gif':
                    $image = imagecreatefromgif($file_path);
                    break;
                default:
                    return $upload;
            }
            
            if (!$image) {
                return $upload;
            }
            
            // パレット画像をTrueColorに変換（WebP対応のため）
            if (!imageistruecolor($image)) {
                $width = imagesx($image);
                $height = imagesy($image);
                $truecolor_image = imagecreatetruecolor($width, $height);
                
                // 透明度を保持
                imagealphablending($truecolor_image, false);
                imagesavealpha($truecolor_image, true);
                
                // パレット画像をTrueColorに変換
                imagecopy($truecolor_image, $image, 0, 0, 0, 0, $width, $height);
                imagedestroy($image);
                $image = $truecolor_image;
            }
            
            // WebPファイルパスを生成
            $path_info = pathinfo($file_path);
            $webp_path = $path_info['dirname'] . '/' . $path_info['filename'] . '.webp';
            
            // WebP形式で保存（品質90%）
            $webp_success = imagewebp($image, $webp_path, 90);
            
            if ($webp_success && file_exists($webp_path)) {
                // WebP変換成功時のみ元ファイルを削除
                unlink($file_path);
                
                // アップロード情報を更新
                $upload['file'] = $webp_path;
                $upload['type'] = 'image/webp';
                $upload['url'] = str_replace(basename($upload['url']), basename($webp_path), $upload['url']);
            }
            
            imagedestroy($image);
            
        } catch (Exception $e) {
            error_log('WebP conversion failed: ' . $e->getMessage());
        }
        
        return $upload;
    }
    
    /**
     * 画像圧縮機能
     *
     * @param array $metadata メタデータ
     * @param int $attachment_id 添付ファイルID
     * @return array 処理済みメタデータ
     */
    public static function compress_image(array $metadata, int $attachment_id = 0): array
    {
        if (!isset($metadata['file'])) {
            return $metadata;
        }
        
        $upload_dir = wp_upload_dir();
        $file_path = $upload_dir['basedir'] . '/' . $metadata['file'];
        
        // ファイルが存在しない場合は処理をスキップ
        if (!file_exists($file_path)) {
            return $metadata;
        }
        
        $file_type = wp_check_filetype($file_path)['type'];
        
        // WebPファイルの場合は追加圧縮を実行
        if ($file_type === 'image/webp' && function_exists('imagewebp')) {
            try {
                $image = imagecreatefromwebp($file_path);
                if ($image) {
                    // より高い圧縮率で再保存（品質85%）
                    imagewebp($image, $file_path, 85);
                    imagedestroy($image);
                }
            } catch (Exception $e) {
                error_log('WebP compression failed: ' . $e->getMessage());
            }
        }
        
        // サムネイルも圧縮
        if (isset($metadata['sizes'])) {
            foreach ($metadata['sizes'] as $size_name => $size_data) {
                $thumbnail_path = dirname($file_path) . '/' . $size_data['file'];
                
                if (file_exists($thumbnail_path) && strpos($size_data['mime-type'], 'image/webp') === 0) {
                    try {
                        $image = imagecreatefromwebp($thumbnail_path);
                        if ($image) {
                            imagewebp($image, $thumbnail_path, 85);
                            imagedestroy($image);
                        }
                    } catch (Exception $e) {
                        error_log('WebP thumbnail compression failed: ' . $e->getMessage());
                    }
                }
            }
        }
        
        return $metadata;
    }
}

// 初期化
ThemeMediaOptimization::init();