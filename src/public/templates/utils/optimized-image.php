<?php
/**
 * 最適化画像コンポーネント
 * 
 * 画像名を渡すだけでRetina対応・次世代フォーマット対応の最適化された画像を出力
 *
 * @package ThemeNameHere
 * @since 1.0.0
 */

// 直接アクセスを防止
if (!defined('ABSPATH')) {
    exit;
}

/**
 * 最適化された画像を出力
 *
 * @param string $image_name 画像名（拡張子なし、例: 'screenshot'）
 * @param array $options オプション配列
 *   - alt: alt属性（デフォルト: ''）
 *   - class: CSSクラス（デフォルト: ''）
 *   - width: 画像の幅（デフォルト: null）
 *   - height: 画像の高さ（デフォルト: null）
 *   - loading: loading属性（デフォルト: 'lazy'）
 *   - sizes: sizes属性（デフォルト: '(max-width: 768px) 100vw, 50vw'）
 *   - fetchpriority: fetchpriority属性（デフォルト: null）
 *   - fallback_format: フォールバック画像形式（デフォルト: 自動検出）
 * @return void
 */
function render_optimized_image(string $image_name, array $options = []): void
{
    // デフォルトオプションの設定
    $defaults = [
        'alt' => '',
        'class' => '',
        'width' => null,
        'height' => null,
        'loading' => 'lazy',
        'sizes' => '(max-width: 768px) 100vw, 50vw',
        'fetchpriority' => null,
        'fallback_format' => null,
    ];
    
    $options = array_merge($defaults, $options);
    
    // 画像のベースURL
    $base_url = get_template_directory_uri() . '/assets/images/';
    $base_path = get_template_directory() . '/assets/images/';
    
    // フォールバック形式の自動検出
    if (empty($options['fallback_format'])) {
        if (file_exists($base_path . $image_name . '@1x.jpg') || file_exists($base_path . $image_name . '@1x.jpeg')) {
            $fallback_format = 'jpg';
        } elseif (file_exists($base_path . $image_name . '@1x.png')) {
            $fallback_format = 'png';
        } else {
            $fallback_format = 'png'; // デフォルト
        }
    } else {
        $fallback_format = $options['fallback_format'];
    }
    
    // 各フォーマットのURL生成
    $formats = [
        'avif' => [
            '1x' => $base_url . $image_name . '@1x.avif',
            '2x' => $base_url . $image_name . '@2x.avif',
        ],
        'webp' => [
            '1x' => $base_url . $image_name . '@1x.webp',
            '2x' => $base_url . $image_name . '@2x.webp',
        ],
        $fallback_format => [
            '1x' => $base_url . $image_name . '@1x.' . $fallback_format,
            '2x' => $base_url . $image_name . '@2x.' . $fallback_format,
        ],
    ];
    
    // 属性の構築
    $attributes = [];
    
    if (!empty($options['class'])) {
        $attributes[] = 'class="' . esc_attr($options['class']) . '"';
    }
    
    if (!empty($options['width'])) {
        $attributes[] = 'width="' . esc_attr($options['width']) . '"';
    }
    
    if (!empty($options['height'])) {
        $attributes[] = 'height="' . esc_attr($options['height']) . '"';
    }
    
    if (!empty($options['loading'])) {
        $attributes[] = 'loading="' . esc_attr($options['loading']) . '"';
    }
    
    if (!empty($options['fetchpriority'])) {
        $attributes[] = 'fetchpriority="' . esc_attr($options['fetchpriority']) . '"';
    }
    
    $img_attributes = implode(' ', $attributes);
    
    // picture要素の出力
    echo '<picture>';
    
    // AVIF source
    echo '<source type="image/avif" ';
    echo 'srcset="' . esc_url($formats['avif']['1x']) . ' 1x, ' . esc_url($formats['avif']['2x']) . ' 2x" ';
    echo 'sizes="' . esc_attr($options['sizes']) . '">';
    
    // WebP source
    echo '<source type="image/webp" ';
    echo 'srcset="' . esc_url($formats['webp']['1x']) . ' 1x, ' . esc_url($formats['webp']['2x']) . ' 2x" ';
    echo 'sizes="' . esc_attr($options['sizes']) . '">';
    
    // フォールバック（PNG/JPEG）
    $fallback_mime_type = $fallback_format === 'jpg' ? 'image/jpeg' : 'image/png';
    echo '<img ';
    echo 'src="' . esc_url($formats[$fallback_format]['1x']) . '" ';
    echo 'srcset="' . esc_url($formats[$fallback_format]['1x']) . ' 1x, ' . esc_url($formats[$fallback_format]['2x']) . ' 2x" ';
    echo 'alt="' . esc_attr($options['alt']) . '" ';
    echo 'sizes="' . esc_attr($options['sizes']) . '" ';
    echo $img_attributes;
    echo '>';
    
    echo '</picture>';
}

/**
 * 最適化された画像のHTMLを取得（出力しない）
 *
 * @param string $image_name 画像名（拡張子なし）
 * @param array $options オプション配列
 * @return string 生成されたHTML
 */
function get_optimized_image(string $image_name, array $options = []): string
{
    ob_start();
    render_optimized_image($image_name, $options);
    return ob_get_clean();
}

/**
 * 背景画像用のCSS変数を生成
 *
 * @param string $image_name 画像名（拡張子なし）
 * @param string $format フォーマット（'avif', 'webp', 'png'）
 * @return string CSS変数の文字列
 */
function get_background_image_css_vars(string $image_name, string $format = 'webp'): string
{
    $base_url = get_template_directory_uri() . '/assets/images/';
    
    $css_vars = [
        '--bg-image-1x: url(' . esc_url($base_url . $image_name . '@1x.' . $format) . ')',
        '--bg-image-2x: url(' . esc_url($base_url . $image_name . '@2x.' . $format) . ')',
    ];
    
    return implode('; ', $css_vars);
}

/**
 * レスポンシブ背景画像のCSSを生成
 *
 * @param string $image_name 画像名（拡張子なし）
 * @return string CSS文字列
 */
function get_responsive_background_css(string $image_name): string
{
    $base_url = get_template_directory_uri() . '/assets/images/';
    $base_path = get_template_directory() . '/assets/images/';
    
    // フォールバック形式の自動検出
    if (file_exists($base_path . $image_name . '@1x.jpg') || file_exists($base_path . $image_name . '@1x.jpeg')) {
        $fallback_format = 'jpg';
    } elseif (file_exists($base_path . $image_name . '@1x.png')) {
        $fallback_format = 'png';
    } else {
        $fallback_format = 'png'; // デフォルト
    }
    
    $css = "
        background-image: url('{$base_url}{$image_name}@1x.{$fallback_format}');
        background-image: url('{$base_url}{$image_name}@1x.webp');
        background-image: url('{$base_url}{$image_name}@1x.avif');
        
        @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
            background-image: url('{$base_url}{$image_name}@2x.{$fallback_format}');
            background-image: url('{$base_url}{$image_name}@2x.webp');
            background-image: url('{$base_url}{$image_name}@2x.avif');
        }
    ";
    
    return trim($css);
}

/**
 * 画像の存在チェック
 *
 * @param string $image_name 画像名（拡張子なし）
 * @param string $format チェックする形式（指定がない場合は利用可能な形式を自動検索）
 * @return bool 画像が存在するかどうか
 */
function optimized_image_exists(string $image_name, string $format = null): bool
{
    $base_path = get_template_directory() . '/assets/images/';
    
    if ($format) {
        // 指定された形式をチェック
        return file_exists($base_path . $image_name . '@1x.' . $format);
    }
    
    // いずれかの形式が存在するかチェック
    $formats = ['png', 'jpg', 'jpeg'];
    foreach ($formats as $fmt) {
        if (file_exists($base_path . $image_name . '@1x.' . $fmt)) {
            return true;
        }
    }
    
    return false;
}