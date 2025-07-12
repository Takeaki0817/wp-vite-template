# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

WordPressテーマ開発用の最小限のスターターキットです。
Vite + TailwindCSS v4 + 画像最適化による高速開発環境を提供します。

## 開発コマンド

```bash
# 開発ワークフロー
npm run dev:boot          # WordPress + Vite初回起動
npm run dev:wp           # WordPress + Vite監視モード
npm run dev              # フロントエンドのみ
npm run build            # 本番ビルド

# WordPress環境管理
npm run wp-env:start     # WordPress Docker起動
npm run wp-env:stop      # WordPress Docker停止
npm run wp-export        # WordPressデータベースエクスポート
npm run wp-import        # WordPressデータベースインポート

# リセットコマンド
npm run reset            # distフォルダと画像キャッシュをクリア
npm run dev:reboot       # 完全リセット後に開発再開
```

**アクセスURL**: WordPress http://localhost:8888、管理画面 http://localhost:8888/wp-admin (admin/password)

## ビルドシステム設計

### Vite設定 (`vite.config.js`)
- **マルチ入力ビルド**: `src/assets/`内のJS/CSSを自動検出
- **モジュール保持**: WordPress用に元のファイル構造を維持
- **開発監視**: `src/assets/`と`src/public/`を監視
- **アセット命名**: WordPressとの互換性のためハッシュなしで元のファイル名を保持

### カスタムViteプラグイン
1. **vite-plugin-sharp**: 高度な画像最適化とキャッシング
   - 複数フォーマット生成: AVIF、WebP、元画像
   - サイズバリエーション: @1x（50%縮小、軽量版）、@2x（元サイズ、高品質版）
   - スマートキャッシュ：変更されていない画像の再処理を回避
   - SVGOによるSVG最適化

2. **vite-plugin-php-minify**: 本番ビルド用PHP圧縮

### TailwindCSS v4統合
- **CSS-first設定**: `src/assets/styles/tailwind.css`
- コンテンツスキャン: `./src/public/**/*.php`、`./src/public/**/*.html`
- `@theme`ブロックでカスタムブランドカラーとデザイントークンを定義

## WordPressテーマ設計

### モジュラー関数読み込み (`src/public/functions.php`)
以下の順序で関数を読み込み:
1. **グローバル設定**: `variables/global-config.php` - `$GLOBALS['site_config']`でアクセス可能
2. **コアモジュール**: theme-setup → security → performance → media-optimization
3. **テンプレートユーティリティ**: optimized-image.php、art-direction-image.php

### テーマクラス設計
- **ThemeSetup**: クラスベースの初期化、静的メソッドでWordPressフックを管理
- **自動初期化**: `ThemeSetup::init()`で`after_setup_theme`と`wp_enqueue_scripts`フックを登録
- **動的バージョニング**: `get_dynamic_version()`で開発/本番環境の適切なキャッシュ管理

### アセット読み込み戦略 (`src/public/functions/theme-setup.php`)
- **動的バージョニング**: 開発環境ではファイル更新時刻、本番環境では固定バージョン
- **ページ固有スクリプト**: WordPressテンプレート階層に基づいて`assets/scripts/pages/`からJSファイルを自動読み込み
- **条件付き読み込み**: マッチするページでのみスクリプトを読み込み（front-page.jsはホームページ、single.jsは投稿ページなど）
- **defer属性**: パフォーマンス向上のためテーマスクリプトに自動追加

### 画像最適化統合
`src/public/templates/utils/`のテンプレートユーティリティ:
- `optimized-image.php`: 複数フォーマットの`<picture>`要素生成
- `art-direction-image.php`: アートディレクション対応レスポンシブ画像

## 開発パターン

### アセット構成
```
src/assets/
├── images/          # dist/assets/images/に自動処理
├── scripts/
│   ├── common.js    # サイト全体の機能
│   └── pages/       # テンプレート固有スクリプト
└── styles/
    ├── tailwind.css # TailwindCSS設定
    └── add-style.css # 追加スタイル
```

### グローバル設定
`src/public/variables/global-config.php`で編集:
- 会社情報と連絡先
- ソーシャルメディアリンク
- 機能切り替え（show_social_links、show_business_hoursなど）

**テンプレート内でのアクセス方法:**
```php
<?php 
global $site_config;
echo esc_html($site_config['company']['name']); 
echo esc_html($site_config['company']['phone']); 
if ($site_config['features']['show_social_links']) {
    // ソーシャルリンクを表示
}
?>

### TailwindCSSカスタマイズ
`src/assets/styles/tailwind.css`でブランドカラーを変更:
```css
@theme {
  --color-primary: #2563eb;
  --color-secondary: #7c3aed;
  /* ... */
}
```

## ファイル処理動作

### 画像処理
- **トリガー条件**: タイムスタンプ追跡によるファイル変更検出
- **出力フォーマット**: 各画像に対して元画像、WebP、AVIF
- **サイズバリエーション**: @1x（50%縮小、軽量版）、@2x（元サイズ、高品質版）
- **キャッシング**: MD5ハッシュベースで変更されていないファイルをスキップ
- **開発時**: ファイル変更時のリアルタイム処理

### ビルド出力構造
```
dist/
├── assets/
│   ├── images/      # 複数フォーマットの最適化画像
│   ├── scripts/     # 構造を保持してコンパイルされたJS
│   └── styles/      # コンパイルされたCSS
└── *.php            # WordPressテンプレートファイル（本番では圧縮）
```

## WordPress統合ノート

- **ナビゲーションメニュー**: WordPress管理画面で'primary'と'footer'メニューを登録
- **テーマサポート**: アイキャッチ画像、タイトルタグ、HTML5、レスポンシブ埋め込み、ブロックエディタ機能を含む
- **セキュリティ**: 直接ファイルアクセスを防止、適切なWordPressフックを使用
- **パフォーマンス**: 画像最適化、スクリプトのdefer、キャッシュバスティングを実装

## 画像ユーティリティ関数

### 基本的な最適化画像の表示
```php
<?php render_optimized_image('hero-image', [
    'alt' => 'ヒーロー画像の説明',
    'class' => 'w-full h-auto',
    'loading' => 'eager', // ヒーロー画像の場合
    'sizes' => '100vw'
]); ?>
```

### 画像の存在チェック
```php
if (optimized_image_exists('hero-image')) {
    render_optimized_image('hero-image', $options);
} else {
    echo '<div class="placeholder">画像が見つかりません</div>';
}
```

### 背景画像用CSS変数の生成
```php
<div style="<?php echo get_background_image_css_vars('hero-bg', 'webp'); ?>">
    <!-- コンテンツ -->
</div>
```

## 重要な開発ノート

### ファイル命名規則
- **画像ファイル**: 元ファイル名で`src/assets/images/`に配置。処理後は`@1x`（軽量版）、`@2x`（高品質版）が自動生成
- **ページ固有スクリプト**: `src/assets/scripts/pages/`に配置。ファイル名がページ条件と自動マッチング
  - `front-page.js` → ホームページ
  - `single.js` → 投稿ページ
  - `archive.js` → アーカイブページ
  - `404.js` → 404ページ

### ビルドプロセスの理解
- **開発モード**: ファイル変更監視 + 画像リアルタイム処理
- **本番モード**: PHP圧縮 + アセット最適化
- **キャッシュ無効化**: 開発環境では動的バージョニング、本番環境では`style.css`更新時刻

### デバッグとトラブルシューティング

**画像が表示されない場合:**
1. `src/assets/images/`に元画像が存在するか確認
2. `dist/assets/images/`に処理済み画像（@1x/@2x）が生成されているか確認
3. `npm run reset && npm run build`でキャッシュクリア

**スクリプトが読み込まれない場合:**
1. ファイルパスとページ条件が正しくマッチしているか確認
2. `ThemeSetup::enqueue_page_specific_scripts()`のロジックを参照
3. ブラウザ開発者ツールでネットワークタブを確認

**ビルドエラーの場合:**
- Viteプラグインのエラー: `plugins/vite-plugin-sharp.js`、`plugins/vite-plugin-php-minify.js`をチェック
- 依存関係の問題: `npm install`を再実行
- Docker環境の問題: `npm run wp-env:stop && npm run wp-env:start`