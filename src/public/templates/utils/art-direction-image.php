<?php
/**
 * アートディレクション画像コンポーネント
 * 
 * アートディレクション（異なるブレークポイントで異なる画像を表示）に対応した
 * 最適化画像コンポーネント
 *
 * @package WpViteTheme
 * @since 1.0.0
 */

// 直接アクセスを防止
if (!defined('ABSPATH')) {
    exit;
}

/**
 * アートディレクション対応の最適化画像を出力
 *
 * @param array $images 画像設定の配列
 *   [
 *     'mobile' => [
 *       'image' => 'image-mobile',
 *       'media' => '(max-width: 767px)',
 *       'sizes' => '100vw'
 *     ],
 *     'tablet' => [
 *       'image' => 'image-tablet', 
 *       'media' => '(min-width: 768px) and (max-width: 1023px)',
 *       'sizes' => '50vw'
 *     ],
 *     'desktop' => [
 *       'image' => 'image-desktop',
 *       'media' => '(min-width: 1024px)',
 *       'sizes' => '33vw'
 *     ]
 *   ]
 * @param array $options オプション配列
 *   - alt: alt属性（デフォルト: ''）
 *   - class: CSSクラス（デフォルト: ''）
 *   - width: 画像の幅（デフォルト: null）
 *   - height: 画像の高さ（デフォルト: null）
 *   - loading: loading属性（デフォルト: 'lazy'）
 *   - fetchpriority: fetchpriority属性（デフォルト: null）
 *   - fallback_format: フォールバック画像形式（デフォルト: 自動検出）
 *   - fallback_breakpoint: フォールバック画像に使用するブレークポイント（デフォルト: 'desktop'）
 * @return void
 */
function render_art_direction_image(array $images, array $options = []): void
{
    // デフォルトオプションの設定
    $defaults = [
        'alt' => '',
        'class' => '',
        'width' => null,
        'height' => null,
        'loading' => 'lazy',
        'fetchpriority' => null,
        'fallback_format' => null,
        'fallback_breakpoint' => 'desktop',
    ];
    
    $options = array_merge($defaults, $options);
    
    if (empty($images)) {
        echo '<!-- アートディレクション用の画像が提供されていません -->';
        return;
    }

    // ブレークポイントの正しい順序を定義（mobile → tablet → desktop）
    $breakpoint_order = ['mobile', 'tablet', 'desktop'];

    // 順序に従ってソート
    $sorted_images = [];
    foreach ($breakpoint_order as $bp) {
        if (isset($images[$bp])) {
            $sorted_images[$bp] = $images[$bp];
        }
    }
    // 未定義のブレークポイントも追加
    foreach ($images as $bp => $config) {
        if (!isset($sorted_images[$bp])) {
            $sorted_images[$bp] = $config;
        }
    }
    $images = $sorted_images;

    // 画像のベースURL
    $base_url = get_template_directory_uri() . '/assets/images/';
    $base_path = get_template_directory() . '/assets/images/';
    
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
    
    // フォールバック画像の特定
    if (!empty($options['fallback_breakpoint']) && isset($images[$options['fallback_breakpoint']])) {
        $fallback_image = $images[$options['fallback_breakpoint']];
    } else {
        $fallback_image = end($images);
        reset($images);
    }
    
    // フォールバック形式の自動検出
    if (empty($options['fallback_format'])) {
        if (file_exists($base_path . $fallback_image['image'] . '@1x.jpg') || file_exists($base_path . $fallback_image['image'] . '@1x.jpeg')) {
            $fallback_format = 'jpg';
        } elseif (file_exists($base_path . $fallback_image['image'] . '@1x.png')) {
            $fallback_format = 'png';
        } else {
            $fallback_format = 'png'; // デフォルト
        }
    } else {
        $fallback_format = $options['fallback_format'];
    }
    
    // picture要素の出力開始
    echo '<picture>';
    
    // 各ブレークポイント用のsource要素を出力
    foreach ($images as $breakpoint => $config) {
        $image_name = $config['image'];
        $media_query = $config['media'] ?? '';
        $sizes = $config['sizes'] ?? '100vw';
        
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
        ];
        
        // AVIF source
        echo '<source ';
        if (!empty($media_query)) {
            echo 'media="' . esc_attr($media_query) . '" ';
        }
        echo 'type="image/avif" ';
        echo 'srcset="' . esc_url($formats['avif']['1x']) . ' 1x, ' . esc_url($formats['avif']['2x']) . ' 2x" ';
        echo 'sizes="' . esc_attr($sizes) . '">';
        
        // WebP source
        echo '<source ';
        if (!empty($media_query)) {
            echo 'media="' . esc_attr($media_query) . '" ';
        }
        echo 'type="image/webp" ';
        echo 'srcset="' . esc_url($formats['webp']['1x']) . ' 1x, ' . esc_url($formats['webp']['2x']) . ' 2x" ';
        echo 'sizes="' . esc_attr($sizes) . '">';
        
        // フォールバック形式のsource
        $fallback_formats = [
            $fallback_format => [
                '1x' => $base_url . $image_name . '@1x.' . $fallback_format,
                '2x' => $base_url . $image_name . '@2x.' . $fallback_format,
            ],
        ];
        
        echo '<source ';
        if (!empty($media_query)) {
            echo 'media="' . esc_attr($media_query) . '" ';
        }
        $fallback_mime_type = $fallback_format === 'jpg' ? 'image/jpeg' : 'image/png';
        echo 'type="' . esc_attr($fallback_mime_type) . '" ';
        echo 'srcset="' . esc_url($fallback_formats[$fallback_format]['1x']) . ' 1x, ' . esc_url($fallback_formats[$fallback_format]['2x']) . ' 2x" ';
        echo 'sizes="' . esc_attr($sizes) . '">';
    }
    
    // フォールバック用のimg要素
    $fallback_sizes = $fallback_image['sizes'] ?? '100vw';
    echo '<img ';
    echo 'src="' . esc_url($base_url . $fallback_image['image'] . '@1x.' . $fallback_format) . '" ';
    echo 'srcset="' . esc_url($base_url . $fallback_image['image'] . '@1x.' . $fallback_format) . ' 1x, ' . esc_url($base_url . $fallback_image['image'] . '@2x.' . $fallback_format) . ' 2x" ';
    echo 'alt="' . esc_attr($options['alt']) . '" ';
    echo 'sizes="' . esc_attr($fallback_sizes) . '" ';
    echo $img_attributes;
    echo '>';
    
    echo '</picture>';
}

/**
 * アートディレクション対応画像のHTMLを取得（出力しない）
 *
 * @param array $images 画像設定の配列
 * @param array $options オプション配列
 * @return string 生成されたHTML
 */
function get_art_direction_image(array $images, array $options = []): string
{
    ob_start();
    render_art_direction_image($images, $options);
    return ob_get_clean();
}

/**
 * シンプルなレスポンシブ画像（同じ画像の異なるサイズ）
 *
 * @param string $image_name 画像名（拡張子なし）
 * @param array $breakpoints ブレークポイント設定
 *   [
 *     'mobile' => ['media' => '(max-width: 767px)', 'sizes' => '100vw'],
 *     'tablet' => ['media' => '(min-width: 768px) and (max-width: 1023px)', 'sizes' => '50vw'],
 *     'desktop' => ['media' => '(min-width: 1024px)', 'sizes' => '33vw']
 *   ]
 * @param array $options オプション配列
 * @return void
 */
function render_responsive_image(string $image_name, array $breakpoints = [], array $options = []): void
{
    // デフォルトのブレークポイント設定
    if (empty($breakpoints)) {
        $breakpoints = [
            'mobile' => ['media' => '(max-width: 767px)', 'sizes' => '100vw'],
            'tablet' => ['media' => '(min-width: 768px) and (max-width: 1023px)', 'sizes' => '50vw'],
            'desktop' => ['media' => '(min-width: 1024px)', 'sizes' => '33vw']
        ];
    }
    
    // 同じ画像名でアートディレクション配列を構築
    $images = [];
    foreach ($breakpoints as $breakpoint => $config) {
        $images[$breakpoint] = [
            'image' => $image_name,
            'media' => $config['media'],
            'sizes' => $config['sizes']
        ];
    }
    
    render_art_direction_image($images, $options);
}

/**
 * アートディレクション用の背景画像CSSを生成
 *
 * @param array $images 画像設定の配列
 * @param string $format 使用するフォーマット（'avif', 'webp', 'png', 'jpg'）
 * @return string CSS文字列
 */
function get_art_direction_background_css(array $images, string $format = 'webp'): string
{
    if (empty($images)) {
        return '';
    }
    
    $base_url = get_template_directory_uri() . '/assets/images/';
    $css_rules = [];
    
    foreach ($images as $breakpoint => $config) {
        $image_name = $config['image'];
        $media_query = $config['media'] ?? '';
        
        if (!empty($media_query)) {
            $css_rules[] = "@media {$media_query} {
                background-image: url('{$base_url}{$image_name}@1x.{$format}');
            }
            @media {$media_query} and (-webkit-min-device-pixel-ratio: 2), {$media_query} and (min-resolution: 192dpi) {
                background-image: url('{$base_url}{$image_name}@2x.{$format}');
            }";
        }
    }
    
    return implode("\n", $css_rules);
}

/**
 * 複数画像の存在チェック
 *
 * @param array $images 画像設定の配列
 * @param string $format チェックする形式（指定がない場合は利用可能な形式を自動検索）
 * @return bool すべての画像が存在するかどうか
 */
function art_direction_images_exist(array $images, string $format = null): bool
{
    if (empty($images)) {
        return false;
    }
    
    $base_path = get_template_directory() . '/assets/images/';
    
    foreach ($images as $config) {
        $image_name = $config['image'];
        
        if ($format) {
            // 指定された形式をチェック
            if (!file_exists($base_path . $image_name . '@1x.' . $format)) {
                return false;
            }
        } else {
            // いずれかの形式が存在するかチェック
            $formats = ['avif', 'webp', 'png', 'jpg', 'jpeg'];
            $exists = false;
            foreach ($formats as $fmt) {
                if (file_exists($base_path . $image_name . '@1x.' . $fmt)) {
                    $exists = true;
                    break;
                }
            }
            if (!$exists) {
                return false;
            }
        }
    }
    
    return true;
}