# WordPress + Vite + TailwindCSS Starter

A minimal WordPress theme starter kit with modern development tools.

## Features

- ⚡ **Vite** - Lightning fast HMR and build times
- 🎨 **TailwindCSS v4** - Utility-first CSS framework
- 🖼️ **Image Optimization** - Automatic AVIF/WebP conversion
- 🔒 **Security & Performance** - Built-in best practices
- 📱 **Responsive** - Mobile-first design

## Quick Start

```bash
# Clone and install
git clone [your-repository] my-wordpress-site
cd my-wordpress-site
npm install

# Start development
npm run dev:boot

# Access your site
# http://localhost:8888
# Admin: http://localhost:8888/wp-admin (admin/password)
```

## Development

```bash
# Development with WordPress
npm run dev:wp

# Frontend only
npm run dev

# Production build
npm run build
```

## Customization

### 1. Update Site Configuration

Edit `src/public/variables/global-config.php`:

```php
$site_config = [
  'company' => [
    'name' => 'Your Company Name',
    'email' => 'info@yourcompany.com',
    // ...
  ]
];
```

### 2. Customize Colors

Edit `src/assets/styles/tailwind.css`:

```css
@theme {
  --color-primary: #your-color;
  --color-secondary: #your-color;
}
```

### 3. WordPress Menus

Create menus in WordPress admin:
- **Primary Navigation** - Main header menu
- **Footer Navigation** - Footer links

## Project Structure

```
src/
├── assets/
│   ├── images/      # Images (auto-optimized)
│   ├── scripts/     # JavaScript
│   └── styles/      # CSS files
└── public/          # WordPress theme files
    ├── functions/   # PHP modules
    ├── templates/   # Reusable components
    └── *.php        # WordPress templates
```

## Requirements

- Node.js 18+
- Docker (for WordPress environment)

## License

MIT