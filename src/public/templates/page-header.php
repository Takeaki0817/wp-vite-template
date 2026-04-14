<?php
/**
 * ページヘッダーコンポーネント
 *
 * @param array $args {
 *   @type string $title ページタイトル（省略時は current page title）
 * }
 */
if (!defined('ABSPATH')) {
  exit();
}

$title = $args['title'] ?? get_the_title();
?>
<div
  class="from-primary to-secondary bg-linear-to-l px-4 pt-[9.375rem] pb-4 lg:pt-60 lg:pb-7.5"
>
  <div class="mx-auto w-full max-w-(--container-width-md)">
    <h1
      id="js-animation-page-heading"
      class="text-lg font-bold text-white md:text-2xl"
    >
      <?php echo esc_html($title); ?>
    </h1>
  </div>
</div>
