<?php get_header(); ?>

<main>
  <!-- 404エラーページ -->
  <section class="section-py flex min-h-screen flex-col justify-center">
    <div class="section-container text-center">
      <!-- 404番号 -->
      <div class="mb-10">
        <h1 class="text-gray-800 text-[8rem] leading-none font-bold md:text-[12rem] lg:text-[16rem]">
          404
        </h1>
        <div class="relative -mt-8 md:-mt-12 lg:-mt-16">
          <span class="text-gray-400 text-2xl font-bold tracking-wider md:text-3xl lg:text-4xl">
            PAGE NOT FOUND
          </span>
        </div>
      </div>

      <!-- メッセージ -->
      <div class="mb-12 flex flex-col items-center">
        <h2 class="mb-6 text-2xl font-bold text-gray-900 md:text-3xl">
          お探しのページが見つかりません
        </h2>
        <p class="text-gray-600 text-lg leading-relaxed">
          申し訳ございませんが、お探しのページは存在しないか、<br class="hidden md:inline" />
          移動または削除された可能性があります。
        </p>
      </div>

      <!-- トップに戻るボタン -->
      <div class="flex justify-center">
        <a href="<?php echo esc_url(home_url('/')); ?>">
          <?php get_template_part('templates/ui-button', null, [
            'button_text' => 'トップページへ戻る',
            'button_variant' => 'primary'
          ]); ?>
        </a>
      </div>
    </div>
  </section>
</main>

<?php get_footer(); ?>
