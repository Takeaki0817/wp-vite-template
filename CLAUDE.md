# CLAUDE.md

WordPressテーマ開発用スターターキット。Vite + TailwindCSS v4 + 画像最適化による高速開発環境。

## 開発コマンド

```bash
npm run dev:boot      # WordPress + Vite初回起動
npm run dev:wp        # WordPress + Vite監視モード
npm run build         # 本番ビルド
npm run reset         # キャッシュクリア
npm run dev:reboot    # 完全リセット後に開発再開
```

**アクセス**: http://localhost:8888 | 管理画面: /wp-admin (admin/password)

## アーキテクチャ概要

```
src/
├── assets/
│   ├── images/       → 自動最適化（AVIF/WebP/@1x/@2x生成）
│   ├── scripts/      → common.js + pages/*.js（テンプレート自動マッチ）
│   └── styles/       → tailwind.css（CSS-first設定）
└── public/
    ├── functions/    → theme-setup, security, performance
    ├── templates/    → WordPress テンプレート
    └── variables/    → global-config.php（$site_config）
```

## ビルドシステム

- **Vite**: マルチ入力ビルド、ハッシュなしファイル名維持
- **vite-plugin-sharp**: 画像最適化（AVIF/WebP/@1x/@2x）+ キャッシュ
- **vite-plugin-php-minify**: 本番PHP圧縮
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

## トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| 画像未表示 | `npm run reset && npm run build` |
| スクリプト未読込 | ファイル名とテンプレート名の一致確認 |
| ビルドエラー | `npm install` 再実行 |
| Docker問題 | `npm run wp-env:stop && npm run wp-env:start` |

---

## MCP サーバー

| サーバー | 用途 |
|----------|------|
| **figma-remote-mcp** | Figmaデザインシステム連携（デザイン取得、Code Connect） |
| **serena** | LSPベースのシンボルナビゲーション、リファクタリング |

## 利用可能なSkills

### デザイン・スタイリング
| Skill | 用途 |
|-------|------|
| `figma-to-tailwind` | Figma MCPで取得したデザイン変数をTailwind CSSクラスに変換 |
| `create-design-system-rules` | プロジェクト固有のデザインシステムルール生成 |

### コード品質
| Skill | 用途 |
|-------|------|
| `accessibility-auditor` | WCAG準拠チェック、ARIA実装、インクルーシブデザイン |
| `wcag-audit-patterns` | WCAG 2.2アクセシビリティ監査（自動テスト + 手動検証） |
| `seo-review` | SEO最適化監査、検索可視性向上 |
| `serena` | シンボルレベルのコード理解とナビゲーション（LSP） |

### ワークフロー最適化
| Skill | 用途 |
|-------|------|
| `context-compression` | コンテキスト圧縮、長時間セッション最適化 |
| `worktree-agents` | 並列実装オーケストレーション（git worktree使用） |
| `skill-creator` | 新規スキル作成ガイド |

## Subagent推奨

| Agent | 用途 |
|-------|------|
| **Explore** | 大規模コードベースのナビゲーション、ファイル検索 |
| **Plan** | マルチファイル機能の実装計画立案 |
| **Bash** | Git操作、ビルド/テストコマンド実行 |

## 推奨ワークフロー

### Figma→実装フロー
1. `figma-remote-mcp` でデザインコンテキスト取得
2. `figma-to-tailwind` でTailwindクラスに変換
3. 実装後に `accessibility-auditor` でアクセシビリティチェック

### 複雑な機能実装
1. `Plan` agent で実装計画策定
2. `worktree-agents` で並列処理（複数タスク時）
3. `serena` でシンボルレベルのリファクタリング

### コード調査
- `Explore` agent で未知のコードベース探索
- `serena` skill でシンボル参照・定義検索
