<?php
/**
 * CTAセクション
 * single.php / archive.php から呼び出される
 */
if (!defined('ABSPATH')) {
  exit();
}

global $site_config;
$company_name = $site_config['company']['name'] ?? get_bloginfo('name');
$contact_url = $site_config['company']['contact_url'] ?? home_url('/contact');
?>
<section
  class="from-primary to-secondary bg-linear-to-r px-4 py-15 text-white lg:py-20"
>
  <div class="mx-auto w-full max-w-(--container-width-md) text-center">
    <h2 class="mb-4 text-2xl font-bold md:text-3xl">
      <?php echo esc_html($company_name); ?>
      にお気軽にご相談ください
    </h2>
    <p class="mb-8 text-lg opacity-90">
      サービスに関するご質問・お見積りはお気軽にお問い合わせください。
    </p>
    <?php get_template_part('templates/ui-button', null, [
      'button_text' => 'お問い合わせ',
      'button_variant' => 'white',
      'href' => esc_url($contact_url),
      'class' => 'px-8 py-3 text-base',
    ]); ?>
  </div>
</section>
