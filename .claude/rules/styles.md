---
globs: ["src/assets/styles/**/*.css"]
---

# CSS/TailwindCSS Patterns

## TailwindCSS v4 CSS-first 構成

エントリーファイル `src/assets/styles/tailwind.css` に全設定を集約する。

```css
@import 'tailwindcss';
@source '../../public/**/*.php';     /* コンテンツソース */
@plugin '@tailwindcss/typography';   /* プラグイン */
@theme { /* デザイントークン */ }
```

## @theme — デザイントークン定義

ブランドカラー・フォント・スペーシング等のプロジェクト固有値は `@theme` に定義する。
定義した変数はそのまま Tailwind ユーティリティクラスになる（例: `--color-primary` → `bg-primary`）。
CSS カスタムプロパティとしても `max-w-(--container-width-md)` 構文で参照可能。

## @utility — カスタムユーティリティ定義ルール

テンプレートで繰り返し使うクラスの組み合わせは `@utility` で定義する。

### 必須ルール

1. **`tailwind.css` 内に書く** — `@import 'tailwindcss'` がないファイルは TailwindCSS コンテキスト外で処理され、`@utility` が展開されずブラウザに生のまま渡る
2. **内部は `@apply` で Tailwind クラスを使う** — 生の CSS プロパティではなく `@apply` でユーティリティクラスを合成する
3. **レスポンシブは `@apply` 内のプレフィックスで対応** — `@media` を手書きせず `sm:` / `lg:` 等のプレフィックスを使う

### 書き方

```css
/* Good: @apply + Tailwind クラスで定義 */
@utility my-component {
  @apply w-full mx-auto px-4 sm:px-6 lg:px-8 lg:max-w-7xl;
}

/* Bad: 生の CSS プロパティ */
@utility my-component {
  width: 100%;
  margin-left: auto;
  padding-left: 1rem;
}

/* Bad: @layer components（v3 の書き方） */
@layer components {
  .my-component { @apply ...; }
}
```

### 定義すべきケース

- 3 箇所以上のテンプレートで同じクラスの組み合わせが繰り返される場合
- レイアウト・タイポグラフィ・カードなどデザインシステムの基本単位

### 定義すべきでないケース

- 1-2 箇所でしか使わない → テンプレート側で直接ユーティリティクラスを使う
- バリエーションが多い → `@theme` のデザイントークンで対応する

## ファイル構成

```
src/assets/styles/
├── tailwind.css    # @theme + @source + @plugin + @utility すべてここ
└── add-style.css   # WP管理画面からの上書きスタイル転記専用（開発用スタイルを書かない）
```
