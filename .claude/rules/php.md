---
globs: ["src/public/**/*.php"]
---

# WordPress PHP Patterns

## Coding Standards

- Use WordPress Coding Standards for PHP
- Always escape output: `esc_html()`, `esc_attr()`, `esc_url()`
- Sanitize input: `sanitize_text_field()`, `wp_kses_post()`
- Use nonces for form security: `wp_nonce_field()`, `wp_verify_nonce()`

## ThemeSetup Class Pattern

```php
class ThemeSetup {
    public static function init(): void {
        add_action('after_setup_theme', [__CLASS__, 'setup']);
        add_action('wp_enqueue_scripts', [__CLASS__, 'enqueue_scripts']);
    }

    public static function setup(): void {
        // Theme supports here
    }
}
ThemeSetup::init();
```

## Hook Usage

- Use `add_action()` and `add_filter()` for WordPress hooks
- Prefer static methods with `[__CLASS__, 'method_name']` syntax
- Common hooks: `after_setup_theme`, `wp_enqueue_scripts`, `init`

## Modular Function Loading

Functions are loaded in order from `src/public/functions/`:
1. `variables/global-config.php` - Global settings
2. `theme-setup.php` - Core setup
3. `security.php` - Security measures
4. `performance.php` - Performance optimizations
5. `media-optimization.php` - Media handling

## Security

- Prevent direct file access: `if (!defined('ABSPATH')) exit;`
- Use `wp_enqueue_script()` / `wp_enqueue_style()` for assets
- Never trust user input without validation
