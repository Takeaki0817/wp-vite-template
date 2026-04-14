<?php
/**
 * ニュース一覧アイテムコンポーネント
 * archive.php の記事ループ内で使用
 *
 * @param array $args {
 *   @type WP_Post $post 投稿オブジェクト
 * }
 */
if (!defined('ABSPATH')) {
  exit();
}

$post = $args['post'] ?? null;
if (!$post) {
  return;
}

setup_postdata($post);
$permalink = get_permalink($post->ID);
$title = get_the_title($post->ID);
$date = get_the_date('Y/m/d', $post->ID);
$excerpt = wp_trim_words(get_the_excerpt($post->ID), 60, '…');
$has_thumb = has_post_thumbnail($post->ID);
?>
<a
  href="<?php echo esc_url($permalink); ?>"
  class="group flex gap-4 rounded-lg border border-gray-200 bg-white p-4 transition-shadow hover:shadow-md md:gap-6 md:p-5"
>
  <?php if ($has_thumb) : ?>
  <div class="h-20 w-28 shrink-0 overflow-hidden rounded md:h-24 md:w-36">
    <?php echo get_the_post_thumbnail($post->ID, 'card', [
      'class' =>
        'h-full w-full object-cover transition-transform duration-300 group-hover:scale-105',
    ]); ?>
  </div>
  <?php endif; ?>
  <div class="flex min-w-0 flex-col justify-center gap-1">
    <time datetime="<?php echo esc_attr(get_the_date('Y-m-d', $post->ID)); ?>" class="text-xs text-gray-400">
      <?php echo esc_html($date); ?>
    </time>
    <h2
      class="group-hover:text-primary truncate font-semibold text-gray-900 md:text-lg"
    >
      <?php echo esc_html($title); ?>
    </h2>
    <?php if ($excerpt) : ?>
    <p class="line-clamp-2 text-sm text-gray-500"><?php echo esc_html($excerpt); ?></p>
    <?php endif; ?>
  </div>
</a>
