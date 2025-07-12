<header class="sticky top-0 z-50 bg-white shadow-md">
  <div class="container-fluid">
    <div class="flex items-center justify-between h-16">
      <!-- Logo -->
      <div class="flex-shrink-0">
        <a href="<?php echo esc_url(home_url('/')); ?>" class="flex items-center text-xl font-bold text-gray-900">
          <?php if (has_custom_logo()): ?>
            <?php the_custom_logo(); ?>
          <?php else: ?>
            <?php echo esc_html(get_bloginfo('name')); ?>
          <?php endif; ?>
        </a>
      </div>
      
      <!-- Navigation -->
      <nav class="hidden md:flex items-center space-x-8">
        <?php
        wp_nav_menu([
          'theme_location' => 'primary',
          'container' => false,
          'menu_class' => 'flex items-center space-x-6',
          'fallback_cb' => false,
          'link_before' => '<span class="nav-link">',
          'link_after' => '</span>',
        ]);
        ?>
      </nav>
      
      <!-- Mobile menu button -->
      <button type="button" class="md:hidden p-2 text-gray-600 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary/20 rounded-lg" id="mobile-menu-toggle">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
        </svg>
      </button>
    </div>
    
    <!-- Mobile Navigation -->
    <nav class="md:hidden hidden" id="mobile-menu">
      <div class="py-4 border-t border-gray-200">
        <?php
        wp_nav_menu([
          'theme_location' => 'primary',
          'container' => false,
          'menu_class' => 'space-y-2',
          'fallback_cb' => false,
          'link_before' => '<span class="block px-4 py-2 text-gray-700 hover:text-primary hover:bg-gray-50 rounded-lg transition-colors">',
          'link_after' => '</span>',
        ]);
        ?>
      </div>
    </nav>
  </div>
</header>

<script>
// Simple mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
  const toggle = document.getElementById('mobile-menu-toggle');
  const menu = document.getElementById('mobile-menu');
  
  if (toggle && menu) {
    toggle.addEventListener('click', function() {
      menu.classList.toggle('hidden');
    });
  }
});
</script>