<?php get_header(); ?>

<main>
  <!-- Hero Section -->
  <section class="bg-gradient-to-br from-primary to-secondary text-white">
    <div class="container-fluid py-20 lg:py-32 text-center">
      <h1 class="text-display mb-6">
        Welcome to Your Site
      </h1>
      <p class="text-xl lg:text-2xl mb-8 max-w-2xl mx-auto opacity-90">
        A modern WordPress starter template with Vite and TailwindCSS
      </p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <?php get_template_part('templates/ui-button', null, [
          'button_text' => 'Get Started',
          'button_variant' => 'white',
          'href' => '/about',
          'class' => 'px-8 py-3'
        ]); ?>
        <?php get_template_part('templates/ui-button', null, [
          'button_text' => 'Learn More',
          'button_variant' => 'outline',
          'href' => '#features',
          'class' => 'px-8 py-3 border-white text-white hover:bg-white hover:text-primary'
        ]); ?>
      </div>
    </div>
  </section>

  <!-- Features Section -->
  <section id="features" class="section-padding">
    <div class="container-fluid">
      <h2 class="text-heading text-center mb-12">Key Features</h2>
      
      <div class="grid md:grid-cols-3 gap-8">
        <div class="card text-center">
          <div class="w-12 h-12 bg-primary/10 text-primary rounded-lg flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold mb-2">Fast Development</h3>
          <p class="text-gray-600">Vite-powered with HMR for instant feedback</p>
        </div>
        
        <div class="card text-center">
          <div class="w-12 h-12 bg-secondary/10 text-secondary rounded-lg flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4z"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold mb-2">Modern Styling</h3>
          <p class="text-gray-600">TailwindCSS v4 with custom design system</p>
        </div>
        
        <div class="card text-center">
          <div class="w-12 h-12 bg-success/10 text-success rounded-lg flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold mb-2">Production Ready</h3>
          <p class="text-gray-600">Optimized builds with image optimization</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Content Section -->
  <section class="section-padding bg-gray-50">
    <div class="container-fluid">
      <div class="max-w-3xl mx-auto text-center">
        <h2 class="text-heading mb-6">Start Building Today</h2>
        <p class="text-body mb-8">
          This starter template provides everything you need to build modern WordPress themes 
          with the latest web technologies. Customize it to fit your needs and deploy with confidence.
        </p>
        <?php get_template_part('templates/ui-button', null, [
          'button_text' => 'View Documentation',
          'button_variant' => 'primary',
          'href' => 'https://github.com/your-repo',
          'class' => 'px-6 py-3'
        ]); ?>
      </div>
    </div>
  </section>
</main>

<?php get_footer(); ?>