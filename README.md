# WordPress + Vite + TailwindCSS v4 スターターキット

![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=flat-square&logo=node.js&logoColor=white)
![PHP](https://img.shields.io/badge/PHP-8.1+-777BB4?style=flat-square&logo=php&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-v4-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-8.x-646CFF?style=flat-square&logo=vite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)

Vite + TailwindCSS v4 + 画像自動最適化を組み合わせた WordPress テーマ開発用スターターキットです。ローカル環境は `@wordpress/env`（Docker）で即時構築でき、本番ビルドは GitHub Actions で FTP デプロイまで自動化できます。

---

## 目次

- [プロジェクト概要](#プロジェクト概要)
- [必要な環境](#必要な環境)
- [セットアップ手順](#セットアップ手順)
- [開発コマンド一覧](#開発コマンド一覧)
- [ディレクトリ構造](#ディレクトリ構造)
- [ビルドシステム](#ビルドシステム)
- [テーマのカスタマイズ](#テーマのカスタマイズ)
- [テンプレート構成](#テンプレート構成)
- [コード整形](#コード整形)
- [デプロイ方法（GitHub Actions FTP）](#デプロイ方法github-actions-ftp)
- [トラブルシューティング](#トラブルシューティング)

---

## プロジェクト概要

### 何のためのスターターキットか

WordPress テーマをゼロから開発する際の繰り返し作業（環境構築・ビルド設定・画像最適化・セキュリティ強化）を省略し、実装に集中できる状態を即時に提供します。

### 技術スタック

| カテゴリ | 採用技術 | 用途 |
|----------|----------|------|
| ビルドツール | Vite 8.x（Rolldown） | JS/CSS バンドル・ウォッチ（10〜30倍高速化） |
| CSS | TailwindCSS v4 | ユーティリティ CSS・デザイントークン |
| 画像最適化 | sharp + カスタムプラグイン | AVIF/WebP/@1x/@2x 自動生成 |
| PHP 圧縮 | カスタム Vite プラグイン | 本番 PHP ファイルの最小化 |
| ローカル環境 | @wordpress/env（Docker） | WordPress + PHP 環境の即時構築 |
| CI/CD | GitHub Actions | FTP 自動デプロイ |
| コード整形 | Prettier + カスタムプラグイン | PHP/HTML 混在テンプレートの自動整形 |

---

## 必要な環境

| 要件 | バージョン | 備考 |
|------|-----------|------|
| **Node.js** | 18.0.0 以上 | `package.json` の `engines` フィールドで指定 |
| **Docker** | 最新版 | Docker Desktop 推奨（@wordpress/env が使用） |
| **PHP** | 8.1 以上 | wp-env 内で自動提供されるため手動インストール不要 |

---

## セットアップ手順

### 1. リポジトリをクローンする

```bash
git clone https://github.com/Takeaki0817/wp-vite-template.git my-theme
cd my-theme
```

### 2. 依存パッケージをインストールする

```bash
npm install
```

### 3. Docker が起動していることを確認する

Docker Desktop を起動してから次のコマンドを実行します。

### 4. WordPress + Vite を一括起動する

```bash
npm run dev:boot
```

このコマンドで `@wordpress/env` が WordPress コンテナを起動し、続いて Vite のウォッチビルドが開始されます。

### 5. ブラウザでアクセスする

| URL | 説明 |
|-----|------|
| `http://localhost:8888` | WordPress フロントエンド |
| `http://localhost:8888/wp-admin` | 管理画面（admin / password） |

### 6. テーマ固有の設定を変更する

`src/public/variables/global-config.php` を開き、会社名・連絡先・SNS URL などを書き換えます（詳細は[テーマのカスタマイズ](#テーマのカスタマイズ)を参照）。

---

## 開発コマンド一覧

| コマンド | 説明 |
|----------|------|
| `npm run dev:boot` | WordPress コンテナ起動 + Vite ウォッチ（初回起動） |
| `npm run dev:wp` | WordPress コンテナ起動 + Vite ウォッチ（2 回目以降） |
| `npm run build` | 本番ビルド（`dist/` に出力） |
| `npm run reset` | `dist/` と画像キャッシュを削除 |
| `npm run dev:reboot` | 完全リセット後に開発再開 |
| `npm run wp-env:start` | WordPress コンテナのみ起動 |
| `npm run wp-env:stop` | WordPress コンテナを停止 |
| `npm run wp-export` | DB を `sql/wpenv.sql` にエクスポート |
| `npm run wp-import` | `sql/wpenv.sql` を DB にインポート |
| `npm run format` | PHP テンプレートを整形 |
| `npm run format:check` | 整形チェック（CI 用、未整形なら exit 1） |

---

## ディレクトリ構造

```
wp-vite-template/
├── src/
│   ├── assets/
│   │   ├── images/          # 元画像を配置（AVIF/WebP/@1x/@2x を自動生成）
│   │   ├── scripts/
│   │   │   ├── common.js    # 全ページ共通スクリプト
│   │   │   └── pages/       # ページ固有スクリプト（テンプレートに自動マッチ）
│   │   │       ├── front-page.js
│   │   │       ├── single.js
│   │   │       ├── archive.js
│   │   │       └── 404.js
│   │   └── styles/
│   │       ├── tailwind.css  # TailwindCSS エントリー + @theme + @utility 定義
│   │       └── add-style.css # WP 管理画面上書きスタイル専用
│   └── public/               # WordPress テーマファイル（dist/ にそのままコピー）
│       ├── functions.php     # モジュール読み込みエントリー
│       ├── functions/        # PHP モジュール群
│       │   ├── theme-setup.php        # テーマサポート・アセット登録
│       │   ├── security.php           # セキュリティヘッダー・XML-RPC 無効化
│       │   ├── performance.php        # キャッシュ・wp_head 最適化
│       │   └── media-optimization.php # カスタム画像サイズ・アップロード設定
│       ├── templates/        # パーシャルテンプレート
│       │   ├── ui-button.php      # ボタンコンポーネント
│       │   ├── page-header.php    # ページヘッダー
│       │   ├── cta.php            # CTA セクション
│       │   ├── news-item.php      # ニュース一覧アイテム
│       │   ├── part-header.php    # ヘッダーパーツ
│       │   ├── part-footer.php    # フッターパーツ
│       │   └── utils/             # 画像ユーティリティ関数
│       │       ├── optimized-image.php
│       │       └── art-direction-image.php
│       ├── variables/
│       │   └── global-config.php  # $site_config グローバル設定
│       ├── header.php         # wp_head() 呼び出し
│       ├── footer.php         # wp_footer() 呼び出し
│       ├── front-page.php     # トップページテンプレート
│       ├── single.php         # 投稿詳細テンプレート
│       ├── archive.php        # アーカイブテンプレート
│       ├── page.php           # 固定ページテンプレート
│       ├── 404.php            # 404 テンプレート
│       └── index.php          # フォールバックテンプレート
├── scripts/
│   └── format-wp.mjs         # PHP テンプレートフォーマッター CLI
├── plugins/                  # カスタム Vite プラグイン
│   ├── vite-plugin-sharp.js  # 画像最適化プラグイン
│   ├── vite-plugin-php-minify.js # PHP 圧縮プラグイン
│   └── prettier-plugin-wp-php.mjs # Prettier WP PHP プラグイン
├── dist/                     # ビルド出力（Git 管理外）
├── vite.config.js
├── .wp-env.json
└── package.json
```

---

## ビルドシステム

### Vite の設定概要

Vite 8 は Rolldown（Rust製）をバンドラーとして採用しており、Vite 7 比で **10〜30倍高速なビルド** を実現しています。

`vite.config.js` では以下の方針でビルドを構成しています。

**マルチ入力ビルド**

`fast-glob` で `src/assets/**/*.{js,css}` を動的に検出し、すべてのエントリーポイントを自動登録します。新しいファイルを配置するだけでビルド対象に追加されます。

**ハッシュなしファイル名**

WordPress から `wp_enqueue_script()` / `wp_enqueue_style()` で読み込むため、ファイル名はハッシュなしの元の名前を維持します。

```
dist/assets/scripts/common.js          （ハッシュなし）
dist/assets/styles/tailwind.css        （ハッシュなし）
dist/assets/images/hero@1x.webp        （ハッシュなし）
```

**開発モードのウォッチ**

`NODE_ENV=development` のときは `src/assets/**` と `src/public/**` を監視し、変更時に即時リビルドします。

### 画像最適化（vite-plugin-sharp）

`src/assets/images/` に画像を配置すると、ビルド時に以下のバリエーションが `dist/assets/images/` に自動生成されます。

| 入力ファイル | 生成されるファイル |
|-------------|-------------------|
| `hero.jpg` | `hero@1x.jpg`, `hero@2x.jpg`, `hero@1x.webp`, `hero@2x.webp`, `hero@1x.avif`, `hero@2x.avif` |
| `logo.svg` | `logo.svg`（SVGO で最適化のみ、サイズバリエーションなし） |

- `@1x` は元画像の 50% サイズ（モバイル・軽量版）
- `@2x` は元画像の 100% サイズ（デスクトップ・Retina 版）
- AVIF 品質: 50 / WebP 品質: 80 / JPEG 品質: 80
- MD5 ベースのキャッシュにより、変更のない画像は再処理をスキップ

### PHP 圧縮（vite-plugin-php-minify）

`npm run build`（本番ビルド）実行時のみ、`src/public/` 以下の PHP ファイルをコメント削除・空白圧縮して `dist/` に出力します。開発中は読みやすい形式のまま維持されます。

### TailwindCSS v4

`src/assets/styles/tailwind.css` が CSS-first の設定ファイルです。`@theme` ブロックでデザイントークンを定義し、そのままユーティリティクラスとして使えます。

```css
@import "tailwindcss";

@source "../../public/**/*.php";

@plugin "@tailwindcss/typography";

@theme {
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --color-primary: #2563eb;
  --color-secondary: #7c3aed;
  --color-accent: #06b6d4;
  --container-width-md: 48rem;
}
```

---

## テーマのカスタマイズ

### グローバル設定（$site_config）

`src/public/variables/global-config.php` にサイト固有の情報をまとめています。テンプレートのどこからでも `global $site_config;` で参照できます。

```php
// src/public/variables/global-config.php
$site_config = [
  'company' => [
    'name'    => 'Your Company Name',
    'phone'   => '000-0000-0000',
    'email'   => 'info@yourcompany.com',
    'website' => 'https://yourcompany.com',
  ],
  'social' => [
    'twitter'   => 'https://twitter.com/yourcompany',
    'facebook'  => 'https://facebook.com/yourcompany',
    'instagram' => 'https://instagram.com/yourcompany',
  ],
  'features' => [
    'show_social_links'   => true,
    'show_business_hours' => true,
  ],
];
```

テンプレートでの参照例:

```php
global $site_config;
echo esc_html($site_config['company']['name']);
echo esc_url($site_config['social']['twitter']);
```

### カラー・フォントの変更

`src/assets/styles/tailwind.css` の `@theme` ブロックを編集します。変更した CSS 変数は即座にユーティリティクラスとして使えるようになります。

```css
@theme {
  /* ブランドカラーを変更 */
  --color-primary: #e11d48;    /* bg-primary, text-primary, border-primary */
  --color-secondary: #7c3aed;

  /* フォントを変更 */
  --font-sans: 'Noto Sans JP', system-ui, sans-serif;

  /* コンテナ幅を変更 */
  --container-width-md: 60rem;
}
```

### ページ固有 JS の追加

`src/assets/scripts/pages/` にファイルを作成するだけで、WordPress テンプレート階層に基づいて自動的に読み込まれます。

| ファイル名 | 読み込まれるページ |
|-----------|-------------------|
| `front-page.js` | `is_front_page()` |
| `single.js` | `is_single()` |
| `archive.js` | `is_archive()` |
| `page-about.js` | `is_page('about')` |
| `404.js` | `is_404()` |

ファイルの基本構造:

```javascript
// src/assets/scripts/pages/front-page.js
document.addEventListener('DOMContentLoaded', () => {
  // トップページ専用の処理
});
```

### 画像の使い方

`src/assets/images/` に元画像（推奨: 2x 解像度の JPG/PNG）を配置してビルドすると、最適化済みバリエーションが自動生成されます。

**基本的な最適化画像の表示:**

```php
<?php render_optimized_image('hero-image', [
    'alt'     => 'ヒーロー画像',
    'class'   => 'w-full h-auto',
    'loading' => 'eager',    // ファーストビューは eager
    'sizes'   => '100vw',
]); ?>
```

**アートディレクション（画面幅で異なる画像）:**

```php
<?php render_art_direction_image([
    'mobile'  => 'hero-mobile',
    'tablet'  => 'hero-tablet',
    'desktop' => 'hero-desktop',
], [
    'alt'     => 'レスポンシブヒーロー画像',
    'class'   => 'w-full',
    'loading' => 'eager',
]); ?>
```

**画像の存在確認:**

```php
if (optimized_image_exists('hero-image')) {
    render_optimized_image('hero-image', ['alt' => '...']);
}
```

---

## テンプレート構成

### WordPress テンプレートファイル

`src/public/` 直下のファイルが WordPress のテンプレート階層に対応しています。

| ファイル | 用途 |
|----------|------|
| `front-page.php` | トップページ（`is_front_page()`） |
| `single.php` | 投稿詳細ページ |
| `archive.php` | カテゴリ・タグ等のアーカイブ |
| `page.php` | 固定ページ（汎用） |
| `404.php` | 404 エラーページ |
| `index.php` | フォールバック（どのテンプレートにも合致しない場合） |
| `header.php` | `get_header()` で呼び出されるヘッダー |
| `footer.php` | `get_footer()` で呼び出されるフッター |

### パーシャルの使い方

`src/public/templates/` 以下のパーシャルは `get_template_part()` で呼び出します。第 3 引数の配列が `$args` としてパーシャル内に渡されます。

**ui-button — ボタンコンポーネント:**

```php
<?php get_template_part('templates/ui-button', null, [
    'text'           => 'お問い合わせ',
    'button_variant' => 'primary',   // primary | outline | white
    'href'           => home_url('/contact'),
    'class'          => 'px-8 py-3',
]); ?>
```

**page-header — ページタイトルヘッダー:**

```php
<?php get_template_part('templates/page-header', null, [
    'title' => get_the_title(),    // 省略時も get_the_title() を使用
]); ?>
```

**cta — CTA セクション（お問い合わせ誘導）:**

`$site_config['company']['name']` と `$site_config['company']['contact_url']` を自動参照します。引数は不要です。

```php
<?php get_template_part('templates/cta'); ?>
```

**news-item — ニュース一覧アイテム:**

```php
<?php while (have_posts()) : the_post(); ?>
    <?php get_template_part('templates/news-item', null, [
        'post' => $post,
    ]); ?>
<?php endwhile; ?>
```

### ヘッダー・フッターパーツ

`templates/part-header.php` と `templates/part-footer.php` はそれぞれサイト共通のナビゲーションとフッターコンテンツを担当します。`header.php` / `footer.php` から呼び出されます。

---

## コード整形

PHP/HTML 混在テンプレートを安全に整形するための専用 Prettier プラグイン（`prettier-plugin-wp-php.mjs`）を搭載しています。

### 動作方式

| PHP ファイルの種類 | 整形方法 |
|-------------------|---------|
| 閉じタグなし（純粋 PHP） | Prettier の `php` パーサーでファイル全体を整形 |
| テンプレート（PHP/HTML 混在） | PHP ブロックを退避 → HTML を整形 → PHP を個別整形して復元 |

- `<?php ... ?>` / `<?= ... ?>` は単一の HTML タグとして扱われる
- `<!DOCTYPE>`, `<html>`, `<head>`, `<body>` はフラグメント対応のため無視
- Tailwind クラスソートは HTML 属性内で引き続き動作
- `<!-- prettier-ignore -->` は不要

### コマンド

| コマンド | 説明 |
|----------|------|
| `npm run format` | 全 PHP ファイルを整形 |
| `npm run format:check` | 整形が必要なファイルを表示（CI 用、exit 1） |
| `npx prettier --write src/public/file.php` | 単一ファイル整形 |

### VSCode 連携

Prettier 拡張（[esbenp.prettier-vscode](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)）をインストールすれば、保存時に自動整形されます。`.vscode/settings.json` で設定済み。

---

## デプロイ方法（GitHub Actions FTP）

`.github/workflows/deploy.yml` で GitHub Actions による FTP デプロイが設定されています。デフォルトでは手動実行（`workflow_dispatch`）のみ有効です。

### GitHub Secrets の設定手順

1. GitHub のリポジトリページで **Settings** を開く
2. 左メニューの **Secrets and variables → Actions** を選択
3. **New repository secret** ボタンから以下の 5 つを登録する

| Secret 名 | 値の例 | 説明 |
|-----------|--------|------|
| `FTP_HOST` | `ftp.example.com` | FTP サーバーのホスト名 |
| `FTP_USERNAME` | `your-ftp-username` | FTP ユーザー名 |
| `FTP_PASSWORD` | `your-ftp-password` | FTP パスワード |
| `FTP_PORT` | `21` | FTP ポート（省略時は 21） |
| `FTP_SERVER_DIR` | `public_html/wp-content/themes/my-theme/` | サーバー側のアップロード先パス |

`.env.example` を参考に値を確認できます。

```bash
cp .env.example .env
# .env を編集して各値を確認
```

### ワークフローの手動実行方法

1. GitHub リポジトリの **Actions** タブを開く
2. 左メニューの **Deploy to FTP** を選択
3. **Run workflow** ボタンをクリック → ブランチを選択して **Run workflow** を実行

ワークフローは以下の順序で処理されます。

1. リポジトリをチェックアウト
2. Node.js 20 をセットアップ（`npm ci` で依存解決）
3. `npm run build` を実行
4. `dist/` 以下を FTP でサーバーに転送

### デプロイされるファイルについて

`dist/` 以下のすべてのファイルが `FTP_SERVER_DIR` に転送されます。`.sharp-cache.json`（画像キャッシュファイル）と `.git*` 関連ファイルは自動的に除外されます。

```
dist/                          ← このディレクトリの内容がサーバーに転送される
├── assets/images/             # 最適化済み画像（AVIF/WebP/@1x/@2x）
├── assets/scripts/            # バンドル済み JS
├── assets/styles/             # コンパイル済み CSS
├── functions.php              # 圧縮済み PHP
├── functions/                 # 圧縮済み PHP モジュール
├── templates/                 # 圧縮済みパーシャル
├── variables/                 # 圧縮済み設定ファイル
└── *.php                      # 圧縮済み WordPress テンプレート
```

### プッシュ時の自動デプロイに変更する方法

現状は手動実行のみですが、`main` ブランチへのプッシュで自動デプロイしたい場合は `.github/workflows/deploy.yml` の `on:` セクションを以下のように変更します。

```yaml
# 変更前（手動実行のみ）
on:
  workflow_dispatch:

# 変更後（main へのプッシュで自動実行）
on:
  push:
    branches:
      - main
```

---

## トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| 画像が表示されない | `npm run reset && npm run build` を実行して画像を再生成する |
| スクリプトが読み込まれない | `pages/` 内のファイル名と WordPress テンプレート名の一致を確認する |
| TailwindCSS が反映されない | `npm run dev:wp` で Vite を再起動する |
| ビルドエラーが発生する | `npm install` を再実行する |
| Docker が起動しない | Docker Desktop の起動を確認後、`npm run wp-env:stop && npm run wp-env:start` を実行する |
| Hot Reload が効かない | Vite を再起動してブラウザキャッシュをクリアする |
| PHP エラーが出る | `global $site_config;` の宣言漏れや、`if (!defined('ABSPATH')) exit;` の記述を確認する |
| GitHub Actions でデプロイ失敗 | Secrets の値（特に `FTP_SERVER_DIR` の末尾スラッシュ）を確認する |
| メニューが表示されない | WordPress 管理画面（外観 → メニュー）でメニュー位置を設定する |
| 整形で PHP が崩れる | `npm run format` を実行して再整形する |

---

## ライセンス

MIT
