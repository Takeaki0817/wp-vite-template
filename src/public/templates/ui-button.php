<?php
/**
 * UIボタンコンポーネント
 *
 * @param array $args {
 *   @type string $text          ボタンテキスト（または button_text でも可）
 *   @type string $button_text   ボタンテキスト（後方互換）
 *   @type string $button_variant バリアント: primary|outline|white（デフォルト: primary）
 *   @type string $href          リンクURL（指定時は <a> タグ）
 *   @type string $class         追加CSSクラス
 *   @type string $type          ボタンタイプ（デフォルト: button）
 * }
 */
if (!defined('ABSPATH')) {
  exit();
}

$text = $args['text'] ?? ($args['button_text'] ?? 'Button');
$variant = $args['button_variant'] ?? 'primary';
$href = $args['href'] ?? '';
$extra = $args['class'] ?? '';
$type = $args['type'] ?? 'button';

$variant_classes = match ($variant) {
  'outline'
    => 'border-2 border-primary text-primary hover:bg-primary hover:text-white',
  'white' => 'bg-white text-primary hover:bg-gray-100',
  default => 'bg-primary text-white hover:bg-blue-700',
};

$base =
  'inline-flex items-center justify-center px-4 py-2 text-sm font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 transition-colors duration-200';
$class = esc_attr(trim("{$base} {$variant_classes} {$extra}"));
?>
<?php if ($href) : ?>
<a href="<?php echo esc_url($href); ?>" class="<?php echo $class; ?>"><?php echo esc_html($text); ?></a>
<?php else : ?>
<button type="<?php echo esc_attr($type); ?>" class="<?php echo $class; ?>">
  <?php echo esc_html($text); ?>
</button>
<?php endif; ?>
