# CLAUDE.md

WordPressテーマ開発用スターターキット。Vite + TailwindCSS v4 + 画像最適化による高速開発環境。

## 開発コマンド

```bash
npm run dev:boot      # WordPress + Vite初回起動
npm run dev:wp        # WordPress + Vite監視モード
npm run build         # 本番ビルド
npm run reset         # キャッシュクリア
npm run dev:reboot    # 完全リセット後に開発再開
npm run format        # PHPテンプレート整形
npm run format:check  # 整形チェック（CI用）
```

**アクセス**: http://localhost:8888 | 管理画面: /wp-admin (admin/password)

## アーキテクチャ概要

```
src/
├── assets/
│   ├── images/       → 自動最適化（AVIF/WebP/@1x/@2x生成）
│   ├── scripts/      → common.js + pages/*.js（テンプレート自動マッチ）
│   └── styles/       → tailwind.css（CSS-first + @utility）+ add-style.css（WP管理画面上書き専用）
└── public/
    ├── functions/    → theme-setup, security, performance, media-optimization
    ├── templates/    → WordPress テンプレート + パーシャル（ui-button, cta, page-header, news-item）
    └── variables/    → global-config.php（$site_config）
scripts/
└── format-wp.mjs     → PHPテンプレート整形スクリプト
plugins/
└── prettier-plugin-wp-php.mjs  → PHP/HTML混在ファイル対応Prettierカスタムプラグイン
.github/workflows/    → deploy.yml（手動FTPデプロイ）
```

## ビルドシステム

- **Vite 8（Rolldown）**: Rust製バンドラーで10〜30倍高速、マルチ入力ビルド、ハッシュなしファイル名維持
- **vite-plugin-sharp**: 画像最適化（AVIF/WebP/@1x/@2x）+ キャッシュ
- **vite-plugin-php-minify**: 本番PHP圧縮（文字列リテラル保護付き — `'...'` / `"..."` / ヒアドキュメントを退避してからコメント・空白削除）
- **TailwindCSS v4**: `@theme`ブロックでカスタマイズ

## 主要パターン

### グローバル設定アクセス
```php
global $site_config;
echo $site_config['company']['name'];
```

### 画像ユーティリティ
```php
render_optimized_image('hero-image', ['alt' => '説明', 'loading' => 'eager']);
```

### ページ固有スクリプト
`scripts/pages/`にファイル配置 → テンプレートに自動マッチ
- `front-page.js` → ホームページ
- `single.js` → 投稿ページ

## 詳細ルール

詳細パターンは `.claude/rules/` を参照:
- `php.md` - WordPress/PHPパターン
- `javascript.md` - JSパターン
- `styles.md` - TailwindCSS設定
- `images.md` - 画像最適化詳細

## コード整形

Prettier + カスタムプラグイン（`plugins/prettier-plugin-wp-php.mjs`）でPHP/HTML混在ファイルを安全に整形する。

- PHP テンプレートの `<?php ?>` タグを含む複雑な構造も崩さずに整形
- VSCode Format on Save に対応（Prettier 拡張のみ必要、追加設定不要）
- `<!-- prettier-ignore -->` は不要（プラグインが自動的に対応）
- 整形対象: `src/public/templates/**/*.php`

```bash
npm run format        # 整形実行
npm run format:check  # 整形チェックのみ（CI/差分確認用）
```

## デプロイ（GitHub Actions FTP）

`.github/workflows/deploy.yml` — `workflow_dispatch`（手動）トリガー

```bash
# 自動デプロイに変更する場合: deploy.yml の on: を以下に書き換える
on:
  push:
    branches:
      - main
```

**GitHub Secrets 設定** (Settings → Secrets and variables → Actions):

| Secret | 説明 |
|--------|------|
| `FTP_HOST` | FTPサーバーホスト |
| `FTP_USERNAME` | FTPユーザー名 |
| `FTP_PASSWORD` | FTPパスワード |
| `FTP_PORT` | FTPポート（デフォルト21） |
| `FTP_SERVER_DIR` | アップロード先パス（例: `public_html/wp-content/themes/my-theme/`） |

## トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| 画像未表示 | `npm run reset && npm run build` |
| スクリプト未読込 | ファイル名とテンプレート名の一致確認 |
| ビルドエラー | `npm install` 再実行 |
| Docker問題 | `npm run wp-env:stop && npm run wp-env:start` |
| 整形で崩れる | `npm run format` で再整形、`npm run format:check` でCI確認 |

---

## 利用可能なスキル

### WordPress専用スキル（プロジェクトローカル）

| スキル | 用途 |
|--------|------|
| **wordpress-router** | WordPressコードベースのルーティング・調査起点 |
| **wp-block-development** | Gutenbergブロック開発（block.json, register_block_type） |
| **wp-block-themes** | ブロックテーマ開発・theme.json設定 |
| **wp-plugin-development** | プラグイン設計・アクティベーション・フック |
| **wp-rest-api** | REST APIエンドポイント構築・拡張 |
| **wp-interactivity-api** | Interactivity API（data-wp-*ディレクティブ） |
| **wp-abilities-api** | WordPress Abilities API |
| **wp-performance** | パフォーマンス最適化（バックエンド） |
| **wp-phpstan** | PHPStan静的解析設定・実行 |
| **wp-wpcli-and-ops** | WP-CLI操作・search-replace・移行 |
| **wp-env** | @wordpress/env ローカル環境管理（グローバル） |
| **wp-playground** | WordPress Playgroundによる検証 |
| **wp-project-triage** | WordPressリポジトリの俯瞰調査 |
| **wpds** | WordPress Design Systemコンポーネント |
| **blueprint** | Playground Blueprint JSON作成 |
| **wcag-audit-patterns** | WCAG 2.2アクセシビリティ監査 |
| **tailwind-css** | TailwindCSS v4ユーティリティ |
| **find-docs** | ライブラリ最新ドキュメント取得（Context7） |

## MCP サーバー

| サーバー | 用途 |
|----------|------|
| **figma-remote-mcp** | Figmaデザインシステム連携（デザイン取得、Code Connect） |

## サブエージェント活用

| タスク | 推奨エージェント |
|--------|-----------------|
| コードベース探索・パターン検索 | Explore |
| 複数ファイルにまたがる実装計画 | Plan |
| 複雑なワークフロー・調査 | general-purpose |