---
globs: ["src/assets/styles/**/*.css"]
---

# CSS/TailwindCSS Patterns

## TailwindCSS v4 Configuration

Main config in `src/assets/styles/tailwind.css`:

```css
@import "tailwindcss";

@theme {
    --color-primary: #2563eb;
    --color-secondary: #7c3aed;
    --color-accent: #f59e0b;
    /* Design tokens */
}
```

## @theme Syntax (v4)

Define design tokens in `@theme` block:

```css
@theme {
    /* Colors */
    --color-brand: #1a1a1a;

    /* Spacing */
    --spacing-section: 4rem;

    /* Typography */
    --font-heading: "Noto Sans JP", sans-serif;
}
```

## Usage in Templates

```html
<div class="bg-primary text-white p-section">
    <h1 class="font-heading text-2xl">Title</h1>
</div>
```

## Responsive Design

Use Tailwind breakpoints:
- `sm:` (640px+)
- `md:` (768px+)
- `lg:` (1024px+)
- `xl:` (1280px+)
- `2xl:` (1536px+)

## File Organization

```
src/assets/styles/
├── tailwind.css    # Main Tailwind config + @theme
└── add-style.css   # Additional custom styles
```

## Best Practices

- Prefer utility classes over custom CSS
- Use `@apply` sparingly for repeated patterns
- Define brand colors in `@theme` block
- Use CSS custom properties for dynamic values
