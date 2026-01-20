---
globs: ["src/assets/images/**"]
---

# Image Optimization Patterns

## File Naming

Place images in `src/assets/images/` with descriptive names:
- `hero-image.jpg` -> Generates `hero-image@1x.webp`, `hero-image@2x.webp`, etc.
- Use lowercase, hyphens for spaces
- Avoid special characters

## Auto-Generated Variants

Each image generates:
- `@1x` - 50% size (lightweight)
- `@2x` - Original size (high quality)

Formats generated:
- Original format
- WebP
- AVIF

## render_optimized_image Usage

```php
<?php render_optimized_image('hero-image', [
    'alt' => 'Description of image',
    'class' => 'w-full h-auto',
    'loading' => 'lazy',      // or 'eager' for above-fold
    'sizes' => '(max-width: 768px) 100vw, 50vw'
]); ?>
```

## Art Direction Pattern

For different images at breakpoints:

```php
<?php render_art_direction_image([
    'mobile' => 'hero-mobile',
    'tablet' => 'hero-tablet',
    'desktop' => 'hero-desktop'
], [
    'alt' => 'Responsive hero image',
    'class' => 'w-full'
]); ?>
```

## Background Images

```php
<div style="<?php echo get_background_image_css_vars('bg-image', 'webp'); ?>">
    <!-- Content -->
</div>
```

## Best Practices

- Use `loading="eager"` only for above-fold images
- Always provide meaningful `alt` text
- Use `optimized_image_exists()` before rendering
- Keep source images at 2x resolution for retina
