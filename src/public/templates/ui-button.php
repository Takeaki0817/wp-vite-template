<!-- prettier-ignore -->
<?php
/**
 * シンプルボタンコンポーネント
 * 
 * @param string $text ボタンのテキスト内容
 * @param string $href リンクURL（指定された場合は<a>タグとしてレンダリング）
 * @param string $class 追加のCSSクラス
 * @param string $type <button>タグのボタンタイプ (button|submit|reset)
 */

// デフォルト値で引数を抽出
$text = $args['text'] ?? 'Button';
$href = $args['href'] ?? '';
$custom_class = $args['class'] ?? '';
$type = $args['type'] ?? 'button';

// Tailwind CSSを使用したデフォルトボタンクラス
$class_string = 'inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-200 ' . $custom_class;

// ボタンまたはリンクをレンダリング
if ($href) {
    // リンクとしてレンダリング
    ?>
    <!-- prettier-ignore -->
    <a href="<?php echo esc_url($href); ?>" class="<?php echo esc_attr($class_string); ?>">
        <?php echo esc_html($text); ?>
    </a>
    <?php
} else {
    // ボタンとしてレンダリング
    ?>
    <!-- prettier-ignore -->
    <button type="<?php echo esc_attr($type); ?>" class="<?php echo esc_attr($class_string); ?>">
        <?php echo esc_html($text); ?>
    </button>
    <?php
}
?>