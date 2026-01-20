# WordPress + Vite + TailwindCSS v4 スターターキット

![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=flat-square&logo=node.js&logoColor=white)
![PHP](https://img.shields.io/badge/PHP-8.1+-777BB4?style=flat-square&logo=php&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-v4-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-7.x-646CFF?style=flat-square&logo=vite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)

最新の開発ツールと高度な最適化機能を備えたWordPressテーマ開発用スターターキットです。

---

## 📑 目次

- [はじめに](#-はじめに)
- [動作要件](#-動作要件)
- [クイックスタート](#-クイックスタート)
- [開発コマンド](#-開発コマンド)
- [プロジェクト構造](#-プロジェクト構造)
- [ビルドシステム設計](#-ビルドシステム設計)
- [画像最適化機能](#-画像最適化機能)
- [TailwindCSS v4設定](#-tailwindcss-v4設定)
- [ページ固有スクリプト](#-ページ固有スクリプト)
- [PHPモジュール詳細](#-phpモジュール詳細)
- [カスタマイズ](#-カスタマイズ)
- [JSライブラリの追加](#-jsライブラリの追加)
- [本番デプロイ](#-本番デプロイ)
- [トラブルシューティング](#-トラブルシューティング)
- [Claude Code連携](#-claude-code連携)
- [MCPサーバー連携](#-mcpサーバー連携)
- [開発者向け情報](#-開発者向け情報)
- [ライセンス](#-ライセンス)

---

## 🌟 はじめに

このスターターキットは、モダンなフロントエンド開発ツールとWordPressを統合し、高速で効率的なテーマ開発環境を提供します。Viteによる超高速なホットリロード、TailwindCSS v4のCSS-first設定、そして自動画像最適化機能により、開発者体験を大幅に向上させます。

セキュリティ強化、パフォーマンス最適化、メディア処理など、本番環境で必要となる機能がすべて組み込まれています。WordPressテンプレート階層に基づいたページ固有スクリプトの自動読み込み、モジュラーなPHP構成により、保守性の高いクリーンなコード構造を維持できます。

---

## 📋 動作要件

| 要件 | バージョン | 備考 |
|------|-----------|------|
| **Node.js** | 18+ | npm同梱 |
| **Docker** | 最新版 | Docker Desktop推奨 |
| **PHP** | 8.1+ | WordPress環境内で自動提供 |
| **WordPress** | 6.0+ | wp-envで自動セットアップ |

---

## 🚀 クイックスタート

```bash
# クローンとインストール
git clone https://github.com/Takeaki0817/wp-vite-template my-wordpress-site
cd my-wordpress-site
npm install

# WordPress + Vite初回セットアップ
npm run dev:boot

# サイトアクセス
# WordPress: http://localhost:8888
# 管理画面: http://localhost:8888/wp-admin (admin/password)
```

---

## 🛠️ 開発コマンド

### メインワークフロー

```bash
npm run dev:boot          # WordPress + Vite初回起動
npm run dev:wp           # WordPress + Vite監視モード
npm run dev              # フロントエンドのみ開発
npm run build            # 本番ビルド
```

### WordPress環境管理

```bash
npm run wp-env:start     # WordPress Docker起動
npm run wp-env:stop      # WordPress Docker停止
npm run wp-export        # WordPressデータベースエクスポート
npm run wp-import        # WordPressデータベースインポート
```

### リセットコマンド

```bash
npm run reset            # distフォルダと画像キャッシュをクリア
npm run dev:reboot       # 完全リセット後に開発再開
```

---

## 📁 プロジェクト構造

```
src/
├── assets/
│   ├── images/          # dist/assets/images/に自動最適化
│   ├── scripts/
│   │   ├── common.js    # サイト全体の機能
│   │   └── pages/       # テンプレート固有スクリプト
│   │       ├── front-page.js
│   │       ├── single.js
│   │       ├── archive.js
│   │       └── 404.js
│   └── styles/
│       ├── tailwind.css # TailwindCSS設定
│       └── add-style.css # 追加スタイル
├── public/              # WordPressテーマファイル
│   ├── functions/       # モジュラーPHP関数
│   │   ├── theme-setup.php
│   │   ├── security.php
│   │   ├── performance.php
│   │   └── media-optimization.php
│   ├── templates/
│   │   └── utils/       # テンプレートユーティリティ
│   │       ├── optimized-image.php
│   │       └── art-direction-image.php
│   ├── variables/
│   │   └── global-config.php # サイト設定
│   └── *.php            # WordPressテンプレート
└── dist/                # ビルド出力（Git管理外）
```

---

## 🏗️ ビルドシステム設計

### Vite設定

- **マルチ入力ビルド**: `src/assets/`内のJS/CSSファイルを自動検出
- **モジュール保持**: WordPress互換性のため元のファイル構造を維持
- **開発監視**: `src/assets/`と`src/public/`ディレクトリを監視
- **アセット命名**: WordPress統合のためハッシュなしで元のファイル名を保持

### カスタムViteプラグイン

#### vite-plugin-sharp（画像最適化）

- **複数フォーマット**: AVIF、WebP、元画像形式を生成
- **サイズバリエーション**: @1x（50%サイズ）、@2x（元サイズ）
- **スマートキャッシュ**: MD5追跡による変更されていない画像の再処理回避
- **SVG最適化**: ベクターグラフィックス用SVGO統合

#### vite-plugin-php-minify

- **本番圧縮**: 本番ビルドでPHPファイルを圧縮
- **開発保持**: 開発中は読みやすい形式を維持

### TailwindCSS v4統合

- **CSS-first設定**: `src/assets/styles/tailwind.css`で定義
- **コンテンツスキャン**: `./src/public/**/*.php`、`./src/public/**/*.html`
- **カスタムデザイントークン**: `@theme`ブロックでブランドカラーとスペーシングを定義

---

## 🖼️ 画像最適化機能

### 自動処理

- **サイズバリエーション**:
  - @1x: 50%縮小サイズ（軽量版、モバイル最適）
  - @2x: 元サイズ（オリジナル、デスクトップ/Retina表示用）
- **フォーマット別処理**:
  - 画像ファイル（JPG/PNG/GIF）: 元画像 + WebP + AVIF（各@1x/@2x）
  - SVGファイル: SVGO最適化のみ（サイズバリエーションなし）
- **品質設定**:
  - AVIF: 品質50（高圧縮）
  - WebP: 品質80（バランス）
  - JPEG: 品質80
  - PNG: 圧縮レベル8
- **スマートキャッシュ**: MD5ベースのファイル変更検出で不要な再処理を防止
- **リアルタイム処理**: 開発中のファイル変更時に画像を最適化

### テンプレート統合

付属のユーティリティで最適化された画像を使用:

```php
// ユーティリティファイルを読み込み（functions.phpで設定済み）

// 基本的な最適化画像
<?php render_optimized_image('hero-image', [
    'alt' => 'ヒーロー画像の説明',
    'class' => 'w-full h-auto',
    'loading' => 'eager', // ヒーロー画像の場合
    'sizes' => '100vw'
]); ?>

// アートディレクション対応（画面サイズ別の異なる画像）
<?php render_art_direction_image([
    'mobile' => [
        'image' => 'hero-mobile',
        'media' => '(max-width: 767px)',
        'sizes' => '100vw'
    ],
    'tablet' => [
        'image' => 'hero-tablet',
        'media' => '(min-width: 768px) and (max-width: 1023px)',
        'sizes' => '50vw'
    ],
    'desktop' => [
        'image' => 'hero-desktop',
        'media' => '(min-width: 1024px)',
        'sizes' => '33vw'
    ]
], [
    'alt' => 'レスポンシブヒーロー画像',
    'class' => 'w-full h-auto',
    'loading' => 'eager'
]); ?>

// シンプルなレスポンシブ画像（同じ画像の異なるサイズ設定）
<?php render_responsive_image('product-image', [
    'mobile' => ['media' => '(max-width: 767px)', 'sizes' => '100vw'],
    'desktop' => ['media' => '(min-width: 768px)', 'sizes' => '50vw']
], [
    'alt' => '商品画像',
    'class' => 'rounded-lg'
]); ?>
```

### 重要な注意事項

#### @1x/@2xファイルについて

- **@1xファイルは軽量版**: 50%縮小サイズでモバイルデバイスや通常表示に最適化
- **@2xファイルは高品質版**: 元サイズでデスクトップやRetina表示に対応
- **命名の理由**: web標準に近い形で@2xが高品質版として機能
- **表示ロジック**: ブラウザが画面密度に応じて自動的に@1xまたは@2xを選択

#### SVGファイルについて

- **サイズバリエーションなし**: SVGファイルはSVGO最適化のみで、@1x/@2xサイズバリエーションは生成されません
- **最適化内容**: 不要なメタデータ削除、コード圧縮、viewBox保持
- **出力**: 元のファイル名のまま最適化されたSVGファイルのみ

#### パフォーマンス最適化の考え方

```html
<!-- 推奨: ブラウザが画面密度に応じて自動選択 -->
<picture>
  <source media="(max-width: 768px)" srcset="hero@1x.avif 1x, hero@2x.avif 2x" type="image/avif">
  <source media="(max-width: 768px)" srcset="hero@1x.webp 1x, hero@2x.webp 2x" type="image/webp">
  <img src="hero@1x.jpg" alt="ヒーロー画像">
</picture>
```

---

## 🎨 TailwindCSS v4設定

### @theme構文

TailwindCSS v4では、デザイントークンを`@theme`ブロックで定義します。これにより、カスタムプロパティとして直接CSSに統合されます。

```css
/* src/assets/styles/tailwind.css */
@import "tailwindcss";

@theme {
    /* カラーパレット */
    --color-primary: #2563eb;
    --color-secondary: #7c3aed;
    --color-accent: #f59e0b;
    --color-brand: #1a1a1a;

    /* タイポグラフィ */
    --font-heading: "Noto Sans JP", sans-serif;
    --font-body: "Noto Sans JP", system-ui, sans-serif;

    /* スペーシング */
    --spacing-section: 4rem;
    --spacing-container: 1.5rem;

    /* ブレークポイント（カスタム） */
    --breakpoint-xs: 375px;
}
```

### デザイントークンの活用

定義したトークンはユーティリティクラスとして使用可能:

```html
<!-- カラー -->
<div class="bg-primary text-white">プライマリ背景</div>
<button class="bg-secondary hover:bg-accent">セカンダリボタン</button>

<!-- タイポグラフィ -->
<h1 class="font-heading text-2xl">見出しフォント</h1>
<p class="font-body">本文フォント</p>

<!-- スペーシング -->
<section class="py-section px-container">セクションスペーシング</section>
```

### CSS-first設定のメリット

1. **直感的な設定**: CSSファイル内で完結
2. **IDEサポート**: CSS変数として認識されるため補完が効く
3. **ランタイム変更**: CSS変数なので動的に変更可能
4. **デバッグ容易**: ブラウザの開発者ツールで確認可能

---

## 📜 ページ固有スクリプト

### 自動読み込みメカニズム

WordPressのテンプレート階層に基づき、対応するスクリプトが自動的に読み込まれます。

```
src/assets/scripts/pages/
├── front-page.js     # is_front_page() → トップページ
├── single.js         # is_single() → 投稿詳細
├── archive.js        # is_archive() → アーカイブ一覧
├── page.js           # is_page() → 固定ページ（汎用）
├── page-about.js     # is_page('about') → 特定の固定ページ
├── 404.js            # is_404() → 404エラーページ
└── contact.js        # カスタムテンプレート用
```

### ファイル命名規則

| ファイル名 | 対応するWordPress関数 | 適用ページ |
|-----------|----------------------|-----------|
| `front-page.js` | `is_front_page()` | ホームページ |
| `single.js` | `is_single()` | 投稿詳細ページ |
| `archive.js` | `is_archive()` | アーカイブページ |
| `page.js` | `is_page()` | 全固定ページ |
| `page-{slug}.js` | `is_page('{slug}')` | 特定の固定ページ |
| `404.js` | `is_404()` | 404ページ |
| `search.js` | `is_search()` | 検索結果ページ |

### 使用例

```javascript
// src/assets/scripts/pages/front-page.js
import Swiper from 'swiper';

document.addEventListener('DOMContentLoaded', () => {
    // トップページ専用のスライダー初期化
    const heroSlider = new Swiper('.hero-slider', {
        slidesPerView: 1,
        autoplay: { delay: 5000 }
    });
});
```

---

## 🧩 PHPモジュール詳細

### ThemeSetup

テーマの基本設定とアセット管理を担当します。

```php
// src/public/functions/theme-setup.php
```

#### 主な機能

| 機能 | 説明 |
|------|------|
| **テーマサポート設定** | `title-tag`, `post-thumbnails`, `html5`, `custom-logo`, `custom-background` |
| **アセット読み込み** | CSS/JSファイルの`wp_enqueue_script/style`による登録 |
| **ページ固有スクリプト** | WordPressテンプレート階層に基づく自動読み込み |
| **defer属性付与** | テーマスクリプトへの`defer`属性自動追加 |
| **ナビゲーションメニュー** | `primary`（ヘッダー）、`footer`（フッター）の登録 |

#### 実装パターン

```php
class ThemeSetup {
    public static function init(): void {
        add_action('after_setup_theme', [__CLASS__, 'setup']);
        add_action('wp_enqueue_scripts', [__CLASS__, 'enqueue_assets']);
    }

    public static function setup(): void {
        // タイトルタグサポート
        add_theme_support('title-tag');

        // アイキャッチ画像
        add_theme_support('post-thumbnails');

        // HTML5マークアップ
        add_theme_support('html5', [
            'search-form', 'comment-form', 'comment-list',
            'gallery', 'caption', 'style', 'script'
        ]);

        // カスタムロゴ
        add_theme_support('custom-logo', [
            'height' => 100,
            'width' => 400,
            'flex-width' => true,
            'flex-height' => true
        ]);

        // ナビゲーションメニュー
        register_nav_menus([
            'primary' => 'プライマリナビゲーション',
            'footer' => 'フッターナビゲーション'
        ]);
    }
}
ThemeSetup::init();
```

---

### ThemeSecurity

セキュリティ強化機能を提供します。

```php
// src/public/functions/security.php
```

#### セキュリティヘッダー

| ヘッダー | 値 | 目的 |
|---------|-----|------|
| `X-Frame-Options` | `SAMEORIGIN` | クリックジャッキング防止 |
| `X-Content-Type-Options` | `nosniff` | MIMEタイプスニッフィング防止 |
| `X-XSS-Protection` | `1; mode=block` | XSS攻撃防止 |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | リファラー情報制御 |
| `Permissions-Policy` | カスタム設定 | ブラウザ機能制限 |

#### 無効化される機能

| 機能 | 理由 |
|------|------|
| **XML-RPC** | 外部攻撃の主要ターゲット |
| **ファイルエディター** | 管理画面からのファイル編集防止 |
| **ユーザー列挙** | `?author=N`による情報漏洩防止 |
| **詳細ログインエラー** | 汎用メッセージに置換 |

#### 実装パターン

```php
class ThemeSecurity {
    public static function init(): void {
        // セキュリティヘッダー
        add_action('send_headers', [__CLASS__, 'send_security_headers']);

        // XML-RPC無効化
        add_filter('xmlrpc_enabled', '__return_false');

        // ファイルエディター無効化
        if (!defined('DISALLOW_FILE_EDIT')) {
            define('DISALLOW_FILE_EDIT', true);
        }

        // ユーザー列挙防止
        add_action('template_redirect', [__CLASS__, 'prevent_user_enumeration']);

        // ログインエラーメッセージ汎用化
        add_filter('login_errors', [__CLASS__, 'generic_login_error']);
    }

    public static function send_security_headers(): void {
        header('X-Frame-Options: SAMEORIGIN');
        header('X-Content-Type-Options: nosniff');
        header('X-XSS-Protection: 1; mode=block');
        header('Referrer-Policy: strict-origin-when-cross-origin');
    }

    public static function generic_login_error(): string {
        return 'ログイン情報が正しくありません。';
    }
}
ThemeSecurity::init();
```

---

### ThemePerformance

パフォーマンス最適化機能を提供します。

```php
// src/public/functions/performance.php
```

#### 最適化機能一覧

| 機能 | 説明 | 効果 |
|------|------|------|
| **バージョン文字列削除** | CSS/JSの`?ver=`パラメータ除去 | キャッシュ効率向上 |
| **キャッシュヘッダー** | 静的ファイルに1年（31536000秒）設定 | リクエスト削減 |
| **絵文字スクリプト無効化** | WordPressデフォルト絵文字無効 | 初期読み込み高速化 |
| **wp_head最適化** | 不要な出力削除 | HTMLサイズ削減 |

#### 削除されるwp_head出力

| 項目 | 関数 | 理由 |
|------|------|------|
| WordPressバージョン | `wp_generator` | セキュリティ向上 |
| RSD（Really Simple Discovery） | `rsd_link` | 未使用機能 |
| WLW Manifest | `wlwmanifest_link` | Windows Live Writer用 |
| ショートリンク | `wp_shortlink_wp_head` | 未使用機能 |
| REST APIディスカバリー | `rest_output_link_wp_head` | 不要な公開情報 |
| oEmbedディスカバリー | `wp_oembed_add_discovery_links` | 不要な公開情報 |
| 絵文字関連 | `print_emoji_*` | パフォーマンス向上 |

#### 実装パターン

```php
class ThemePerformance {
    public static function init(): void {
        // バージョン文字列削除
        add_filter('style_loader_src', [__CLASS__, 'remove_version_strings'], 10, 2);
        add_filter('script_loader_src', [__CLASS__, 'remove_version_strings'], 10, 2);

        // 絵文字無効化
        remove_action('wp_head', 'print_emoji_detection_script', 7);
        remove_action('wp_print_styles', 'print_emoji_styles');

        // wp_head最適化
        remove_action('wp_head', 'wp_generator');
        remove_action('wp_head', 'rsd_link');
        remove_action('wp_head', 'wlwmanifest_link');
        remove_action('wp_head', 'wp_shortlink_wp_head');
        remove_action('wp_head', 'rest_output_link_wp_head');
        remove_action('wp_head', 'wp_oembed_add_discovery_links');
    }

    public static function remove_version_strings($src): string {
        if (strpos($src, '?ver=')) {
            $src = remove_query_arg('ver', $src);
        }
        return $src;
    }
}
ThemePerformance::init();
```

---

### ThemeMediaOptimization

メディア処理とアップロード最適化を担当します。

```php
// src/public/functions/media-optimization.php
```

#### カスタム画像サイズ

| サイズ名 | 幅 | 高さ | 用途 |
|---------|-----|------|------|
| `hero` | 1920px | 1080px | ヒーローセクション |
| `card` | 600px | 400px | カード型コンポーネント |
| `square` | 400px | 400px | サムネイル、アバター |

#### 品質・制限設定

| 設定項目 | 値 | 説明 |
|----------|-----|------|
| **JPEG品質** | 90% | 高品質設定 |
| **WebP自動変換** | 有効 | アップロード時に自動生成 |
| **big_imageしきい値** | 4096px | 自動リサイズの上限 |
| **アップロード上限** | 500MB | 大容量ファイル対応 |
| **メモリ割当** | 512MB | 画像処理用メモリ |

#### LCP最適化

Largest Contentful Paint（LCP）の最適化として、ファーストビュー画像の遅延読み込みを制御:

```php
// LCP対象画像は遅延読み込みを無効化
add_filter('wp_img_tag_add_loading_attr', function($value, $image, $context) {
    // ヒーロー画像など、LCP対象は'eager'に
    if (strpos($image, 'hero') !== false) {
        return 'eager';
    }
    return $value;
}, 10, 3);
```

#### SVGサポート

管理者のみSVGファイルのアップロードを許可:

```php
// SVGサポート（管理者のみ）
add_filter('upload_mimes', function($mimes) {
    if (current_user_can('administrator')) {
        $mimes['svg'] = 'image/svg+xml';
    }
    return $mimes;
});
```

#### 実装パターン

```php
class ThemeMediaOptimization {
    public static function init(): void {
        // カスタム画像サイズ
        add_action('after_setup_theme', [__CLASS__, 'add_image_sizes']);

        // JPEG品質
        add_filter('jpeg_quality', function() { return 90; });

        // big_imageしきい値
        add_filter('big_image_size_threshold', function() { return 4096; });

        // アップロード制限
        add_filter('upload_size_limit', function() { return 500 * 1024 * 1024; });

        // SVGサポート
        add_filter('upload_mimes', [__CLASS__, 'allow_svg_upload']);

        // 遅延読み込み最適化
        add_filter('wp_img_tag_add_loading_attr', [__CLASS__, 'optimize_loading_attr'], 10, 3);
    }

    public static function add_image_sizes(): void {
        add_image_size('hero', 1920, 1080, true);
        add_image_size('card', 600, 400, true);
        add_image_size('square', 400, 400, true);
    }
}
ThemeMediaOptimization::init();
```

---

## 🎨 カスタマイズ

### 1. サイト設定

`src/public/variables/global-config.php`を編集:

```php
$site_config = [
  'company' => [
    'name' => '会社名',
    'email' => 'info@yourcompany.com',
    'phone' => '03-1234-5678',
    'address' => '住所'
  ],
  'social_media' => [
    'facebook' => 'https://facebook.com/yourpage',
    'twitter' => 'https://twitter.com/yourhandle',
    'instagram' => 'https://instagram.com/yourhandle'
  ],
  'features' => [
    'show_social_links' => true,
    'show_business_hours' => true,
    'enable_contact_form' => true
  ]
];
```

### 2. ブランドカラー & デザイントークン

`src/assets/styles/tailwind.css`を編集:

```css
@theme {
  --color-primary: #2563eb;
  --color-secondary: #7c3aed;
  --color-accent: #f59e0b;
  --font-family-sans: 'Noto Sans JP', system-ui, sans-serif;
  --spacing-section: 4rem;
}
```

### 3. WordPressメニュー

WordPress管理画面（外観 → メニュー）でメニューを作成:
- **プライマリナビゲーション** - メインヘッダーメニュー（位置：`primary`）
- **フッターナビゲーション** - フッターリンク（位置：`footer`）

---

## 📦 JSライブラリの追加

プロジェクトに新しいJavaScriptライブラリを追加する方法を説明します。用途に応じて適切な方法を選択してください。

### 方法1: npm管理（推奨）

**使用場面**: モダンなライブラリ、バンドルサイズ最適化が必要な場合

```bash
# ライブラリをインストール
npm install swiper
npm install gsap

# 開発時のみ必要な場合
npm install --save-dev @types/jquery
```

**JSファイルでの使用**:

```javascript
// src/assets/scripts/common.js または pages/*.js
import Swiper from 'swiper';
import { gsap } from 'gsap';

document.addEventListener('DOMContentLoaded', () => {
  // Swiperの初期化
  const swiper = new Swiper('.swiper', {
    direction: 'horizontal',
    loop: true
  });

  // GSAPアニメーション
  gsap.from('.hero-title', {
    duration: 2,
    y: 50,
    opacity: 0
  });
});
```

### 方法2: CDN経由

**使用場面**: 軽量なライブラリ、WordPress依存の強いライブラリ

**theme-setup.php**に追加:

```php
public static function enqueue_assets(): void
{
    // 既存のコード...

    // Alpine.js（CDN）
    wp_enqueue_script(
        'alpinejs',
        'https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js',
        [],
        null,
        false
    );

    // Chart.js（CDN）
    wp_enqueue_script(
        'chartjs',
        'https://cdn.jsdelivr.net/npm/chart.js',
        [],
        '4.4.0',
        false
    );
}
```

### 方法3: ローカルファイル

**使用場面**: カスタマイズしたライブラリ、オフライン対応が必要な場合

```bash
# ライブラリ用ディレクトリを作成
mkdir -p src/assets/scripts/libs

# ライブラリファイルを配置
# 例: src/assets/scripts/libs/custom-slider.js
```

**JSファイルでの使用**:

```javascript
// src/assets/scripts/common.js
import './libs/custom-slider.js';

// または
import { CustomSlider } from './libs/custom-slider.js';
```

### 方法4: ページ固有読み込み

**使用場面**: 特定のページでのみ使用するライブラリ

**ページ固有スクリプトの作成**:

```javascript
// src/assets/scripts/pages/contact.js（お問い合わせページ用）
import { Calendar } from 'vanilla-calendar-picker';

document.addEventListener('DOMContentLoaded', () => {
  // お問い合わせページでのみカレンダーを初期化
  const calendar = new Calendar('#calendar');
});
```

### 動的import（遅延読み込み）

**パフォーマンス最適化**のため、必要な時にライブラリを読み込む:

```javascript
// src/assets/scripts/common.js
document.addEventListener('DOMContentLoaded', () => {
  // モーダルボタンクリック時にライブラリを読み込み
  document.querySelectorAll('.modal-trigger').forEach(button => {
    button.addEventListener('click', async () => {
      const { Modal } = await import('bootstrap');
      const modal = new Modal(document.getElementById('modal'));
      modal.show();
    });
  });
});
```

### 人気ライブラリの追加例

#### Alpine.js（リアクティブUI）

```bash
npm install alpinejs
```

```javascript
// src/assets/scripts/common.js
import Alpine from 'alpinejs';
window.Alpine = Alpine;
Alpine.start();
```

#### Swiper（スライダー）

```bash
npm install swiper
```

```javascript
// src/assets/scripts/pages/front-page.js
import Swiper from 'swiper';
import 'swiper/css';

new Swiper('.hero-slider', {
  slidesPerView: 1,
  autoplay: { delay: 3000 }
});
```

#### GSAP（アニメーション）

```bash
npm install gsap
```

```javascript
// src/assets/scripts/common.js
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);
```

### ライブラリ追加時のトラブルシューティング

#### ライブラリが認識されない場合

1. **npm install後にビルドを再実行**:
   ```bash
   npm run build
   # または
   npm run dev:wp
   ```

2. **Viteの開発サーバーを再起動**:
   ```bash
   # Ctrl+C で停止後
   npm run dev:wp
   ```

#### CSSが読み込まれない場合

```javascript
// CSSも明示的にimport
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
```

#### 外部ライブラリのバンドルサイズ最適化

```javascript
// vite.config.js（必要に応じて）
export default defineConfig({
  build: {
    rollupOptions: {
      external: ['jquery'], // jQueryは外部として扱う
      output: {
        globals: {
          jquery: 'jQuery'
        }
      }
    }
  }
});
```

### 使い分けガイドライン

| 方法 | 適用場面 | メリット | デメリット |
|------|----------|----------|------------|
| **npm管理** | モダンライブラリ、バンドル最適化 | ツリーシェイキング、バージョン管理 | ビルドサイズ増加の可能性 |
| **CDN** | 軽量、すぐに試したい | 高速、キャッシュ効果 | オフライン不可、バージョン管理困難 |
| **ローカル** | カスタマイズ、オフライン | 完全制御、オフライン対応 | 手動管理が必要 |
| **ページ固有** | 特定ページのみ | パフォーマンス最適化 | 管理が複雑 |

---

## 🚀 本番デプロイ

### ビルドコマンド

```bash
# 本番用ビルドを実行
npm run build
```

### ビルド出力

```
dist/
├── assets/
│   ├── images/          # 最適化された画像（AVIF/WebP/@1x/@2x）
│   │   ├── hero@1x.avif
│   │   ├── hero@1x.webp
│   │   ├── hero@2x.avif
│   │   ├── hero@2x.webp
│   │   └── logo.svg
│   ├── scripts/         # コンパイル済みJS
│   │   ├── common.js
│   │   └── pages/
│   └── styles/          # コンパイル済みCSS
│       └── tailwind.css
├── functions/           # PHPモジュール（圧縮済み）
├── templates/
├── variables/
└── *.php                # WordPressテンプレート（圧縮済み）
```

### デプロイ手順

1. **ビルド実行**: `npm run build`
2. **distフォルダをアップロード**: FTP/SFTPでテーマディレクトリへ
3. **テーマ有効化**: WordPress管理画面で有効化

### サーバー要件

| 要件 | 最小バージョン | 推奨バージョン |
|------|---------------|---------------|
| **PHP** | 8.1 | 8.2+ |
| **WordPress** | 6.0 | 6.4+ |
| **WebP対応** | 必須 | - |
| **AVIF対応** | 推奨 | - |

### 本番環境の注意点

- **キャッシュ**: CDNやブラウザキャッシュの設定を確認
- **SSL**: HTTPS必須（混合コンテンツ防止）
- **パーミッション**: wp-contentディレクトリの書き込み権限確認

---

## 🔧 トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| 画像が表示されない | `npm run reset && npm run build` を実行 |
| Dockerが起動しない | Docker Desktop起動確認後 `npm run wp-env:stop && npm run wp-env:start` |
| スクリプトが読み込まれない | ファイル名とWordPressテンプレート名の一致を確認 |
| TailwindCSSが反映されない | Vite再起動 `npm run dev:wp` |
| ビルドエラー | `npm install` を再実行 |
| Hot Reloadが効かない | Vite devサーバー再起動、ブラウザキャッシュクリア |
| 画像が最適化されない | `npm run reset` 後に画像ファイルを再配置 |
| PHPエラー | `global $site_config;` の宣言漏れを確認 |
| メニューが表示されない | WordPress管理画面でメニュー位置を設定 |
| 404ページが表示されない | パーマリンク設定を保存し直す |

### よくある質問

#### Q: 画像の@1xと@2xの違いは？

A: @1xは50%縮小サイズ（軽量版）、@2xは元サイズ（高品質版）です。ブラウザが画面密度に応じて自動選択します。

#### Q: SVGファイルはどう処理される？

A: SVGはサイズバリエーションなしでSVGO最適化のみ実行されます。

#### Q: 新しいページテンプレートを追加するには？

A: `src/public/`に`page-{slug}.php`を作成し、対応する`src/assets/scripts/pages/page-{slug}.js`を追加します。

---

## 🤖 Claude Code連携

このプロジェクトはClaude Code（Anthropic公式CLI）との統合を想定しています。

### CLAUDE.md

プロジェクトルートの`CLAUDE.md`には以下が記載されています:

- 開発コマンドの概要
- アーキテクチャ概要
- ビルドシステムの説明
- 主要パターン（グローバル設定、画像ユーティリティ）
- トラブルシューティング

### .claude/rules/

詳細なコーディング規約が格納されています:

| ファイル | 内容 |
|----------|------|
| `php.md` | WordPressコーディング規約、セキュリティパターン |
| `javascript.md` | ES6+パターン、ページ固有スクリプト規則 |
| `styles.md` | TailwindCSS v4設定、@theme構文 |
| `images.md` | 画像最適化パターン、ユーティリティ関数 |

### .claude/skills/

カスタムSkillsが利用可能です:

| Skill | 用途 |
|-------|------|
| `figma-to-tailwind` | Figmaデザイン変数をTailwindクラスに変換 |
| `accessibility-auditor` | WCAG準拠チェック |
| `wcag-audit-patterns` | WCAG 2.2監査 |
| `seo-review` | SEO最適化監査 |
| `context-compression` | 長時間セッションの最適化 |
| `worktree-agents` | 並列実装オーケストレーション |

---

## 🔌 MCPサーバー連携

Model Context Protocol（MCP）サーバーとの連携により、開発効率を向上させます。

### 初期設定

MCPサーバーを利用するには、`.env`ファイルの設定が必要です。

```bash
# .env.exampleをコピー
cp .env.example .env
```

`.env`ファイルを編集:

```env
# Serena MCP Server
# プロジェクトのルートディレクトリを指定
SERENA_PROJECT_PATH=/Users/your-name/path/to/your-project

# Context7 MCP Server
# Context7のAPIキーを設定（https://context7.com で取得）
CONTEXT7_API_KEY=your-api-key-here
```

#### Context7 APIキーの取得方法

1. [Context7](https://context7.com) にアクセス
2. アカウント作成またはログイン
3. ダッシュボードからAPIキーを発行
4. `.env`ファイルの`CONTEXT7_API_KEY`に設定

#### Serenaプロジェクトパスの設定

`SERENA_PROJECT_PATH`にはプロジェクトの絶対パスを指定します:

```env
# macOS/Linux
SERENA_PROJECT_PATH=/Users/username/projects/your-project

# Windows
SERENA_PROJECT_PATH=C:\Users\username\projects\your-project
```

---

### figma-remote-mcp

Figmaデザインシステムとの連携:

| 機能 | 説明 |
|------|------|
| `get_design_context` | FigmaノードからUIコード生成 |
| `get_screenshot` | Figmaノードのスクリーンショット取得 |
| `get_variable_defs` | デザイン変数の取得 |
| `get_code_connect_map` | コードベースとのマッピング |

### serena

LSP（Language Server Protocol）ベースのコード操作:

| 機能 | 説明 |
|------|------|
| `find_symbol` | シンボル検索（クラス、関数等） |
| `find_referencing_symbols` | 参照箇所の検索 |
| `replace_symbol_body` | シンボル本体の置換 |
| `rename_symbol` | シンボル名の一括変更 |

### context7

ライブラリドキュメントの検索:

| 機能 | 説明 |
|------|------|
| `resolve-library-id` | ライブラリID解決 |
| `query-docs` | ドキュメント検索 |

---

## 👨‍💻 開発者向け情報

### 使用されているWordPressフック

#### アクションフック

| フック | 用途 | ファイル |
|--------|------|----------|
| `after_setup_theme` | テーマサポート設定 | theme-setup.php |
| `wp_enqueue_scripts` | CSS/JS読み込み | theme-setup.php |
| `send_headers` | セキュリティヘッダー送信 | security.php |
| `template_redirect` | ユーザー列挙防止 | security.php |
| `init` | 初期化処理 | 各モジュール |

#### フィルターフック

| フック | 用途 | ファイル |
|--------|------|----------|
| `script_loader_tag` | defer属性追加 | theme-setup.php |
| `style_loader_src` | バージョン文字列削除 | performance.php |
| `script_loader_src` | バージョン文字列削除 | performance.php |
| `xmlrpc_enabled` | XML-RPC無効化 | security.php |
| `login_errors` | ログインエラーメッセージ | security.php |
| `jpeg_quality` | JPEG品質設定 | media-optimization.php |
| `upload_mimes` | SVGサポート | media-optimization.php |
| `big_image_size_threshold` | 画像サイズ上限 | media-optimization.php |

### 新機能追加パターン

#### 1. 新しいPHPモジュールの追加

```php
// src/public/functions/my-feature.php
if (!defined('ABSPATH')) exit;

class MyFeature {
    public static function init(): void {
        add_action('init', [__CLASS__, 'setup']);
    }

    public static function setup(): void {
        // 機能実装
    }
}
MyFeature::init();
```

`functions.php`で読み込み:

```php
require_once get_template_directory() . '/functions/my-feature.php';
```

#### 2. 新しいテンプレートユーティリティの追加

```php
// src/public/templates/utils/my-utility.php
function my_custom_utility($args = []) {
    $defaults = [
        'class' => '',
        'id' => ''
    ];
    $args = wp_parse_args($args, $defaults);

    // 処理
}
```

#### 3. 新しいカスタム投稿タイプの追加

```php
// src/public/functions/custom-post-types.php
class CustomPostTypes {
    public static function init(): void {
        add_action('init', [__CLASS__, 'register_post_types']);
    }

    public static function register_post_types(): void {
        register_post_type('portfolio', [
            'labels' => [
                'name' => 'ポートフォリオ',
                'singular_name' => 'ポートフォリオ'
            ],
            'public' => true,
            'has_archive' => true,
            'supports' => ['title', 'editor', 'thumbnail'],
            'show_in_rest' => true
        ]);
    }
}
CustomPostTypes::init();
```

### ディレクトリ構造の拡張

```
src/public/functions/
├── theme-setup.php        # 既存
├── security.php           # 既存
├── performance.php        # 既存
├── media-optimization.php # 既存
├── custom-post-types.php  # 新規: カスタム投稿タイプ
├── custom-taxonomies.php  # 新規: カスタムタクソノミー
├── shortcodes.php         # 新規: ショートコード
├── widgets.php            # 新規: ウィジェット
└── ajax-handlers.php      # 新規: AJAX処理
```

---

## 📄 ライセンス

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 🔗 アクセスURL

| 項目 | URL |
|------|-----|
| **WordPressサイト** | http://localhost:8888 |
| **WordPress管理画面** | http://localhost:8888/wp-admin |
| **管理者ログイン** | admin / password |
