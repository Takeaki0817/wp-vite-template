<?php
get_header();
get_template_part('templates/page-header', null, ['title' =>
'お知らせ', ]); ?>

<div class="px-4 py-15 lg:py-30">
  <div class="mx-auto w-full max-w-(--container-width-md)">
    <!-- 記事一覧 -->
    <?php if (have_posts()) : ?>
    <ul class="grid grid-cols-1 gap-2.5">
      <?php while (have_posts()) : the_post(); ?>
      <li>
        <!-- prettier-ignore -->
        <?php get_template_part('templates/news-item', null, array('post' => $post)); ?>
      </li>
      <?php endwhile; ?>
    </ul>

    <!-- prettier-ignore -->
    <?php
      // ページネーション
      $pagination_links = paginate_links(array(
        'type' => 'array',
        'prev_text' => '<',
        'next_text' => '>',
        'mid_size' => 2,
        'end_size' => 1,
      ));

      if ($pagination_links) :
      ?>
    <nav class="mt-15 md:mt-20" aria-label="ページネーション">
      <ul class="flex items-center justify-center gap-1.5">
        <?php foreach ($pagination_links as $link) : ?>
        <li>
          <!-- prettier-ignore -->
          <?php
          // current クラスがある場合は現在のページ
          if (strpos($link, 'current') !== false) :
            $page_number = strip_tags($link);
          ?>
          <span
            class="bg-primary flex h-10 w-10 items-center justify-center rounded text-sm font-medium text-white"
          >
            <?php echo $page_number; ?>
          </span>
          <?php else : ?>
          <!-- prettier-ignore -->
          <?php
          // リンクのスタイルを調整
          $styled_link = str_replace(
            'page-numbers',
            'flex h-10 w-10 items-center justify-center rounded bg-gray-300 text-sm font-medium text-white transition-colors hover:bg-primary',
            $link
          );
          echo $styled_link;
          ?>
        <?php endif; ?>
        </li>
        <?php endforeach; ?>
      </ul>
    </nav>
    <!-- prettier-ignore -->
    <?php endif; ?>
    <?php else : ?>
    <!-- 投稿がない場合 -->
    <div class="py-20 text-center">
      <p class="mb-6 text-lg text-gray-600">お知らせはまだありません。</p>
      <a href="<?php echo home_url(); ?>" class="inline-block">
        <!-- prettier-ignore -->
        <?php get_template_part('templates/ui-button', null, [
            'button_text' => 'ホームに戻る',
            'button_variant' => 'primary'
          ]); ?>
      </a>
    </div>
    <?php endif; ?> <?php wp_reset_postdata(); ?>
  </div>
</div>

<?php get_template_part('templates/cta'); get_footer(); ?>
