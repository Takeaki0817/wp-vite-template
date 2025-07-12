<?php
get_header();
?>

<div
  class="from-primary to-secondary bg-linear-to-l px-4 pt-[9.375rem] pb-4 lg:pt-60 lg:pb-7.5"
>
  <div class="mx-auto w-full max-w-(--container-width-md)">
    <div class="">
      <time datetime="<?php the_time('Y-m-d'); ?>" class="text-sm text-white">
        <?php the_time('Y/m/d'); ?>
      </time>
      <h1
        id="js-animation-page-heading"
        class="text-lg font-bold text-white md:text-2xl"
      >
        <?php the_title(); ?>
      </h1>
    </div>
  </div>
</div>

<div class="px-4 py-15 lg:py-30">
  <div class="mx-auto w-full max-w-(--container-width-md)">
    <div class="prose"><?php the_content(); ?></div>
  </div>

  <div class="mt-15 text-center md:mt-30">
    <!-- uibutton -->
    <!-- prettier-ignore -->
    <a href="<?php echo home_url('/news'); ?>" class="inline-block">
      <?php get_template_part('templates/ui-button', null, [
        'button_text' => 'お知らせ一覧に戻る',
        'button_variant' => 'primary',
      ]); ?>
    </a>
  </div>
</div>

<?php get_template_part('templates/cta'); get_footer(); ?>
