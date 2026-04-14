<footer class="mt-20 bg-gray-900 py-12 text-white">
  <div class="container-fluid">
    <!-- Footer Content -->
    <div class="mb-8 grid gap-8 md:grid-cols-3">
      <!-- Company Info -->
      <div>
        <h3 class="mb-4 text-lg font-semibold"><?php echo esc_html(get_bloginfo('name')); ?></h3>
        <p class="mb-4 text-gray-400">
          <?php echo esc_html(get_bloginfo('description')); ?>
        </p>
      </div>

      <!-- Quick Links -->
      <div>
        <h3 class="mb-4 text-lg font-semibold">Quick Links</h3>
        <?php
        wp_nav_menu([
          'theme_location' => 'footer',
          'container' => false,
          'menu_class' => 'space-y-2',
          'fallback_cb' => false,
          'link_before' =>
            '<span class="text-gray-400 hover:text-white transition-colors">',
          'link_after' => '</span>',
        ]);
        ?>
      </div>

      <!-- Contact Info -->
      <div>
        <h3 class="mb-4 text-lg font-semibold">Contact</h3>
        <?php
        global $site_config;
        if (isset($site_config['company'])):
        ?>
        <div class="space-y-2 text-gray-400">
          <?php if (!empty($site_config['company']['email'])): ?>
          <p>
            Email:
            <?php echo esc_html($site_config['company']['email']); ?>
          </p>
          <?php endif; ?>
          <?php if (!empty($site_config['company']['phone'])): ?>
          <p>
            Phone:
            <?php echo esc_html($site_config['company']['phone']); ?>
          </p>
          <?php endif; ?>
        </div>
        <?php endif; ?>
      </div>
    </div>

    <!-- Copyright -->
    <div class="border-t border-gray-800 pt-8 text-center text-gray-400">
      <p>
        &copy;
        <?php echo date('Y'); ?>
        <?php echo esc_html(get_bloginfo('name')); ?>
        . All rights reserved.
      </p>
    </div>
  </div>
</footer>
