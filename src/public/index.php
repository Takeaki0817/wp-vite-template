<?php get_header(); ?>

<div class="container mx-auto px-4 py-8">
  <?php if (have_posts()): ?>
  <div class="grid grid-cols-1 gap-8 md:grid-cols-3">
    <?php while (have_posts()):
    the_post(); ?>
    <div class="overflow-hidden rounded-lg bg-white shadow-lg">
      <?php if (has_post_thumbnail()): ?>
      <a href="<?php the_permalink(); ?>">
        <?php the_post_thumbnail('large', [
          'class' => 'w-full h-48 object-cover',
        ]); ?>
      </a>
      <?php endif; ?>
      <div class="p-6">
        <h2 class="mb-2 text-xl font-bold">
          <a href="<?php the_permalink(); ?>" class="text-gray-900 hover:text-blue-600">
            <?php the_title(); ?>
          </a>
        </h2>
        <p class="mb-4 text-gray-700"><?php echo wp_trim_words(get_the_content(), 20); ?></p>
        <a href="<?php the_permalink(); ?>" class="text-blue-600 hover:underline">
          さらに詳しく見る
        </a>
      </div>
    </div>
    <?php
    endwhile; ?>
  </div>

  <div class="mt-8">
    <?php the_posts_pagination(); ?>
  </div>
  <?php else: ?>
  <p class="text-gray-700">投稿がありません。</p>
  <?php endif; ?>
</div>

<?php get_footer(); ?>
