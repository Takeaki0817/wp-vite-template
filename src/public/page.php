<?php get_header(); ?>

<!-- ページヘッダー -->
<?php get_template_part('templates/page-header'); ?>

<!-- ページコンテンツ -->
<main>
  <div class="mx-auto w-full max-w-(--container-width-md)">
    <?php the_content(); ?>
  </div>
</main>

<?php get_footer(); ?>
