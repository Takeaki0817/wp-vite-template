# WordPress + Vite + TailwindCSS スターター

最新の開発ツールと高度な最適化機能を備えたWordPressテーマ開発用スターターキットです。

## ✨ 特徴

- ⚡ **Vite** - ホットリロード対応の超高速ビルド
- 🎨 **TailwindCSS v4** - カスタムデザイントークン対応のCSS-first設定
- 🖼️ **高度な画像最適化** - スマートキャッシュ機能付きAVIF/WebP変換
- 📱 **レスポンシブ画像** - 複数フォーマット対応のアートディレクション
- 🔒 **セキュリティ & パフォーマンス** - WordPress最適化機能内蔵
- 🧩 **モジュラー設計** - 保守性の高いクリーンなコード構造
- 🚀 **ページ固有アセット** - WordPressテンプレート階層による自動スクリプト読み込み

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

## 🏗️ ビルドシステム設計

### Vite設定
- **マルチ入力ビルド**: `src/assets/`内のJS/CSSファイルを自動検出
- **モジュール保持**: WordPress互換性のため元のファイル構造を維持
- **開発監視**: `src/assets/`と`src/public/`ディレクトリを監視
- **アセット命名**: WordPress統合のためハッシュなしで元のファイル名を保持

### カスタムViteプラグイン

#### vite-plugin-sharp（画像最適化）
- **複数フォーマット**: AVIF、WebP、元画像形式を生成
- **サイズバリエーション**: @1x（フルサイズ）、@2x（パフォーマンス向上のため50%サイズ）
- **スマートキャッシュ**: MD5追跡による変更されていない画像の再処理回避
- **SVG最適化**: ベクターグラフィックス用SVGO統合

#### vite-plugin-php-minify
- **本番圧縮**: 本番ビルドでPHPファイルを圧縮
- **開発保持**: 開発中は読みやすい形式を維持

### TailwindCSS v4統合
- **CSS-first設定**: `src/assets/styles/tailwind.css`で定義
- **コンテンツスキャン**: `./src/public/**/*.php`、`./src/public/**/*.html`
- **カスタムデザイントークン**: `@theme`ブロックでブランドカラーとスペーシングを定義

## 📁 プロジェクト構造

```
src/
├── assets/
│   ├── images/          # dist/assets/images/に自動最適化
│   ├── scripts/
│   │   ├── common.js    # サイト全体の機能
│   │   └── pages/       # テンプレート固有スクリプト
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
```

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

### ⚠️ 重要な注意事項

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

### トラブルシューティング

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

## ⚡ パフォーマンス機能

### アセット読み込み戦略
- **動的バージョニング**: 開発環境ではファイル更新時刻、本番環境では固定バージョン
- **ページ固有スクリプト**: WordPressテンプレート階層による自動読み込み
- **条件付き読み込み**: マッチするページでのみスクリプトを読み込み（例：`front-page.js`はホームページのみ）
- **defer属性**: パフォーマンス向上のためテーマスクリプトに自動追加

### セキュリティ強化
- **直接ファイルアクセス防止**: 適切なWordPressセキュリティヘッダー
- **入力値サニタイズ**: すべてのユーザー入力を適切にエスケープ・検証
- **WordPressフック**: テーマ開発のWordPressベストプラクティスに準拠

## 🔧 ビルド出力

```
dist/
├── assets/
│   ├── images/          # 複数フォーマット最適化画像
│   │   ├── hero@1x.avif      # 50%縮小AVIF（軽量版）
│   │   ├── hero@1x.webp      # 50%縮小WebP（軽量版）
│   │   ├── hero@1x.jpg       # 50%縮小JPEG（軽量版）
│   │   ├── hero@2x.avif      # 元サイズAVIF（高品質版）
│   │   ├── hero@2x.webp      # 元サイズWebP（高品質版）
│   │   ├── hero@2x.jpg       # 元サイズJPEG（高品質版）
│   │   ├── product@1x.png    # 50%縮小PNG（軽量版）
│   │   ├── product@2x.png    # 元サイズPNG（高品質版）
│   │   └── logo.svg          # SVG最適化のみ（サイズバリエーションなし）
│   ├── scripts/         # 構造保持でコンパイルされたJS
│   └── styles/          # コンパイルされたCSS
└── *.php                # WordPressテンプレートファイル（本番では圧縮）
```

## 📋 必要要件

- **Node.js** 18+ 
- **Docker**（WordPress環境用）
- **npm**

## 🚦 開発ワークフロー

1. **初期セットアップ**: `npm run dev:boot` - WordPress + Vite起動
2. **開発継続**: `npm run dev:wp` - 監視モードで継続
3. **アセット変更**: 自動再コンパイルとブラウザリフレッシュ
4. **画像更新**: 自動最適化とキャッシュ無効化
5. **本番**: `npm run build` - 圧縮最適化ビルド

## 📄 ライセンス

MIT License - 詳細はLICENSEファイルを参照

---

**アクセスURL:**
- WordPressサイト: http://localhost:8888
- WordPress管理画面: http://localhost:8888/wp-admin (admin/password)