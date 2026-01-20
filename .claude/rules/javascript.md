---
globs: ["src/assets/scripts/**/*.js"]
---

# JavaScript Patterns

## ES6+ Standards

- Use ES6 modules with `import`/`export`
- Prefer `const` and `let` over `var`
- Use arrow functions for callbacks
- Use template literals for string interpolation

## File Structure

```
src/assets/scripts/
├── common.js          # Site-wide functionality
└── pages/             # Page-specific scripts
    ├── front-page.js  # Homepage
    ├── single.js      # Single posts
    ├── archive.js     # Archive pages
    └── 404.js         # 404 page
```

## Page-Specific Script Naming

Scripts in `pages/` auto-load based on WordPress template:
- `front-page.js` -> `is_front_page()`
- `single.js` -> `is_single()`
- `archive.js` -> `is_archive()`
- `page-{slug}.js` -> Specific page slug

## DOM Ready Pattern

```javascript
document.addEventListener('DOMContentLoaded', () => {
    // Initialize code here
});
```

## Dynamic Imports

```javascript
// Lazy load modules when needed
const loadModule = async () => {
    const { default: module } = await import('./module.js');
    module.init();
};
```

## Best Practices

- Use event delegation for dynamic content
- Debounce scroll/resize handlers
- Clean up event listeners when appropriate
- Use `defer` attribute (auto-added by theme)
