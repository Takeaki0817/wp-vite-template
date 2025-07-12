# Webアクセシビリティ自動チェック・修正ガイド（WordPress/PHP開発向け）

## 概要

このドキュメントは、Claude Codeを使用してWordPressテーマやPHPプロジェクトのアクセシビリティを自動的にチェックし、修正するためのナレッジベースです。JIS X 8341-3:2016の適合レベルAAを基準とし、可能な限り自動検出・修正できる項目に焦点を当てています。

## 重要度の分類

- 🚨 **重大（非干渉）**: 利用者に重大な悪影響を及ぼす - 必ず修正
- ⚠️ **必須**: コンテンツ理解や操作に必須 - 優先的に修正
- 📋 **個別対応**: 状況に応じて確認・修正

---

## 自動チェック・修正項目

### 🚨 重大：非干渉の達成基準

#### 1. 音声の自動再生（1.4.2）

**チェック方法**:

```php
// PHPテンプレート内で自動再生の属性を検出
if (preg_match('/<(audio|video)[^>]*autoplay[^>]*>/i', $content)) {
  // 問題を検出
}
```

**修正例**:

```php
// Before
<video src="<?php echo esc_url($video_url); ?>" autoplay muted>

// After - 再生ボタンとコントロールを追加
<video src="<?php echo esc_url($video_url); ?>" controls>
    <track kind="captions" src="<?php echo esc_url(
      $caption_url
    ); ?>" srclang="ja" label="日本語">
</video>
```

#### 2. キーボードトラップの防止（2.1.2）

**チェック方法**:

```javascript
// functions.phpに追加するチェックスクリプト
document.querySelectorAll('[tabindex]').forEach((element) => {
  if (parseInt(element.getAttribute('tabindex')) > 0) {
    console.warn('positive tabindex detected:', element);
  }
});
```

**修正例**:

```php
// Before - モーダルの実装
<div class="modal" tabindex="-1">
    <div class="modal-content">
        <!-- 閉じるボタンがない -->
    </div>
</div>

// After - エスケープ可能な実装
<div class="modal" tabindex="-1" role="dialog" aria-modal="true">
    <div class="modal-content">
        <button class="modal-close" aria-label="閉じる">×</button>
        <!-- コンテンツ -->
    </div>
</div>
```

### ⚠️ 必須：優先的に対応すべき項目

#### 1. 画像の代替テキスト（1.1.1）

**チェック方法**:

```php
// functions.php - 画像の代替テキストをチェック
add_filter('the_content', function ($content) {
  if (preg_match_all('/<img[^>]+>/i', $content, $matches)) {
    foreach ($matches[0] as $img) {
      if (!preg_match('/alt=["\']([^"\']*)["\']/', $img)) {
        // alt属性が無い画像を検出
        error_log('Missing alt attribute: ' . $img);
      }
    }
  }
  return $content;
});
```

**修正例**:

```php
// カスタム画像出力関数
function output_accessible_image($attachment_id, $size = 'full', $attr = [])
{
  $image_data = wp_get_attachment_image_src($attachment_id, $size);
  $alt_text = get_post_meta($attachment_id, '_wp_attachment_image_alt', true);

  // 代替テキストが無い場合の処理
  if (empty($alt_text)) {
    $alt_text = get_the_title($attachment_id);
    if (empty($alt_text)) {
      $alt_text = ''; // 装飾画像の場合
    }
  }

  $default_attr = [
    'alt' => $alt_text,
    'loading' => 'lazy',
  ];

  $attr = wp_parse_args($attr, $default_attr);

  return wp_get_attachment_image($attachment_id, $size, false, $attr);
}
```

#### 2. 見出し構造の適切な設定（1.3.1, 2.4.6）

**チェック方法**:

```php
// テンプレートファイルの見出し構造をチェック
function check_heading_structure($content)
{
  preg_match_all('/<h([1-6])[^>]*>(.*?)<\/h\1>/i', $content, $headings);

  $previous_level = 0;
  $issues = [];

  foreach ($headings[1] as $index => $level) {
    if ($previous_level > 0 && $level > $previous_level + 1) {
      $issues[] = "見出しレベルが飛んでいます: h{$previous_level} → h{$level}";
    }
    if (empty(trim($headings[2][$index]))) {
      $issues[] = "空の見出しがあります: h{$level}";
    }
    $previous_level = $level;
  }

  return $issues;
}
```

**修正例**:

```php
// Before - 不適切な見出し構造
<h1><?php the_title(); ?></h1>
<h3>サブセクション</h3> <!-- h2を飛ばしている -->
<h4>詳細</h4>

// After - 適切な見出し構造
<h1><?php the_title(); ?></h1>
<?php if (have_posts()):
  while (have_posts()):
    the_post(); ?>
    <article>
        <h2><?php echo esc_html(get_the_category()[0]->name); ?></h2>
        <h3><?php the_title(); ?></h3>
        <?php the_content(); ?>
    </article>
<?php
  endwhile;
endif; ?>
```

#### 3. リンクテキストの明確化（2.4.4）

**チェック方法**:

```php
// 曖昧なリンクテキストを検出
function check_link_text($content)
{
  $vague_texts = [
    'こちら',
    '詳細',
    '続きを読む',
    'クリック',
    'more',
    'click here',
  ];
  $issues = [];

  foreach ($vague_texts as $text) {
    if (
      preg_match('/<a[^>]*>' . preg_quote($text, '/') . '<\/a>/i', $content)
    ) {
      $issues[] = "曖昧なリンクテキスト: {$text}";
    }
  }

  return $issues;
}
```

**修正例**:

```php
// Before
<a href="<?php the_permalink(); ?>">続きを読む</a>

// After - コンテキストを含む明確なテキスト
<a href="<?php the_permalink(); ?>">
    <span class="screen-reader-text"><?php the_title(); ?>の</span>続きを読む
</a>

// またはaria-labelを使用
<a href="<?php the_permalink(); ?>" 
   aria-label="<?php the_title(); ?>の続きを読む">
    続きを読む
</a>
```

#### 4. フォームラベルの関連付け（3.3.2）

**チェック方法**:

```php
// フォーム要素のラベル関連付けをチェック
function check_form_labels($content)
{
  preg_match_all(
    '/<input[^>]+type=["\'](?!hidden|submit|button)[^>]+>/i',
    $content,
    $inputs
  );
  $issues = [];

  foreach ($inputs[0] as $input) {
    if (!preg_match('/id=["\']([^"\']+)["\']/', $input, $id_match)) {
      $issues[] = 'ID属性がないinput要素';
      continue;
    }

    $id = $id_match[1];
    if (
      !preg_match(
        '/<label[^>]+for=["\']' . preg_quote($id, '/') . '["\']/',
        $content
      )
    ) {
      $issues[] = "ラベルが関連付けられていないinput: #{$id}";
    }
  }

  return $issues;
}
```

**修正例**:

```php
// Before - ラベルが関連付けられていない
<div class="form-group">
    <span>お名前</span>
    <input type="text" name="name">
</div>

// After - 適切にラベルを関連付け
<div class="form-group">
    <label for="user-name">お名前 <span class="required">必須</span></label>
    <input type="text" id="user-name" name="name" required aria-required="true">
    <span class="help-text" id="name-help">全角文字で入力してください</span>
</div>
```

#### 5. コントラスト比の確保（1.4.3）

**チェックスクリプト**（functions.phpに追加）:

```php
function add_contrast_checker_script() {
    ?>
    <script>
    // 開発環境でのみ実行
    if (window.location.hostname === 'localhost') {
        function checkContrast(element) {
            const style = window.getComputedStyle(element);
            const bgColor = style.backgroundColor;
            const textColor = style.color;

            // 簡易的なコントラスト比計算（実際はより複雑）
            console.log(`Element contrast - BG: ${bgColor}, Text: ${textColor}`);
        }

        document.querySelectorAll('p, span, h1, h2, h3, h4, h5, h6, a').forEach(checkContrast);
    }
    </script>
    <?php
}
add_action('wp_footer', 'add_contrast_checker_script');
```

**修正例（style.css）**:

```css
/* Before - コントラスト比が低い */
.button-primary {
  background-color: #add8e6; /* 薄い青 */
  color: #ffffff;
}

/* After - コントラスト比4.5:1以上を確保 */
.button-primary {
  background-color: #0066cc; /* 濃い青 */
  color: #ffffff;
}

/* テキストリンクの場合 */
a {
  color: #0066cc; /* 4.5:1以上のコントラスト比 */
  text-decoration: underline; /* 色以外の手がかりも提供 */
}
```

### 📋 個別対応：コンテンツに応じた対応

#### 1. スキップリンクの実装

```php
// header.phpの最初に追加
<body <?php body_class(); ?>>
    <a class="skip-link screen-reader-text" href="#main">
        <?php esc_html_e('メインコンテンツへスキップ', 'textdomain'); ?>
    </a>
    
    <!-- メインコンテンツにIDを付与 -->
    <main id="main" class="site-main">
```

**対応するCSS**:

```css
.skip-link {
  position: absolute;
  left: -9999px;
  top: auto;
  width: 1px;
  height: 1px;
  overflow: hidden;
}

.skip-link:focus {
  position: absolute;
  left: 6px;
  top: 7px;
  z-index: 999999;
  width: auto;
  height: auto;
  padding: 8px 16px;
  background-color: #000;
  color: #fff;
  text-decoration: none;
}
```

#### 2. ARIA属性の適切な使用

```php
// ナビゲーションメニューの実装
<nav aria-label="<?php esc_attr_e('メインメニュー', 'textdomain'); ?>">
    <?php wp_nav_menu([
      'theme_location' => 'primary',
      'menu_id' => 'primary-menu',
      'walker' => new Accessible_Walker_Nav_Menu(), // カスタムウォーカー
    ]); ?>
</nav>

// カスタムウォーカークラス
class Accessible_Walker_Nav_Menu extends Walker_Nav_Menu {
    function start_el(&$output, $item, $depth = 0, $args = array(), $id = 0) {
        $classes = empty($item->classes) ? array() : (array) $item->classes;
        $has_children = in_array('menu-item-has-children', $classes);
        
        $attributes = '';
        if ($has_children) {
            $attributes .= ' aria-haspopup="true" aria-expanded="false"';
        }
        
        // 現在のページの場合
        if (in_array('current-menu-item', $classes)) {
            $attributes .= ' aria-current="page"';
        }
        
        $output .= sprintf(
            '<li class="%s"><a href="%s"%s>%s</a>',
            esc_attr(implode(' ', $classes)),
            esc_url($item->url),
            $attributes,
            esc_html($item->title)
        );
    }
}
```

## WordPressプラグインとの連携

### アクセシビリティチェックの自動化

```php
// functions.phpに追加
add_action('save_post', 'check_post_accessibility', 10, 3);

function check_post_accessibility($post_id, $post, $update)
{
  if (wp_is_post_autosave($post_id) || wp_is_post_revision($post_id)) {
    return;
  }

  $content = $post->post_content;
  $issues = [];

  // 画像の代替テキストチェック
  preg_match_all('/<img[^>]+>/i', $content, $images);
  foreach ($images[0] as $img) {
    if (!preg_match('/alt=["\'][^"\']*["\']/', $img)) {
      $issues[] = '代替テキストがない画像があります';
    }
  }

  // 見出し構造チェック
  $heading_issues = check_heading_structure($content);
  $issues = array_merge($issues, $heading_issues);

  // 問題がある場合は管理者に通知
  if (!empty($issues)) {
    set_transient('accessibility_issues_' . $post_id, $issues, DAY_IN_SECONDS);
  }
}

// 管理画面に警告を表示
add_action('admin_notices', 'show_accessibility_warnings');

function show_accessibility_warnings()
{
  global $post;
  if (!$post) {
    return;
  }

  $issues = get_transient('accessibility_issues_' . $post->ID);
  if ($issues) {
    echo '<div class="notice notice-warning is-dismissible">';
    echo '<p><strong>アクセシビリティの問題:</strong></p>';
    echo '<ul>';
    foreach ($issues as $issue) {
      echo '<li>' . esc_html($issue) . '</li>';
    }
    echo '</ul>';
    echo '</div>';
  }
}
```

## テーマ開発のベストプラクティス

### 1. アクセシブルなテンプレート構造

```php
// single.php の基本構造
<?php get_header(); ?>

<main id="main" class="site-main">
    <?php while (have_posts()):
      the_post(); ?>
        <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
            <header class="entry-header">
                <h1 class="entry-title"><?php the_title(); ?></h1>
                <div class="entry-meta">
                    <time datetime="<?php echo get_the_date('c'); ?>">
                        <?php echo get_the_date(); ?>
                    </time>
                </div>
            </header>
            
            <div class="entry-content">
                <?php the_content(); ?>
            </div>
            
            <footer class="entry-footer">
                <?php
                // カテゴリーとタグを適切にマークアップ
                $categories = get_the_category_list(', ');
                if ($categories) {
                  printf(
                    '<div class="cat-links"><span class="screen-reader-text">%s</span>%s</div>',
                    esc_html__('カテゴリー:', 'textdomain'),
                    $categories
                  );
                }
                ?>
            </footer>
        </article>
    <?php
    endwhile; ?>
</main>

<?php get_footer(); ?>
```

### 2. JavaScriptでの動的コンテンツ対応

```javascript
// アクセシブルなタブ実装
class AccessibleTabs {
  constructor(container) {
    this.container = container;
    this.tabs = container.querySelectorAll('[role="tab"]');
    this.panels = container.querySelectorAll('[role="tabpanel"]');

    this.init();
  }

  init() {
    this.tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => this.selectTab(index));
      tab.addEventListener('keydown', (e) => this.handleKeydown(e, index));

      // 初期状態の設定
      if (index === 0) {
        tab.setAttribute('aria-selected', 'true');
        tab.setAttribute('tabindex', '0');
      } else {
        tab.setAttribute('aria-selected', 'false');
        tab.setAttribute('tabindex', '-1');
      }
    });
  }

  selectTab(index) {
    // すべてのタブを非選択状態に
    this.tabs.forEach((tab, i) => {
      tab.setAttribute('aria-selected', 'false');
      tab.setAttribute('tabindex', '-1');
      this.panels[i].hidden = true;
    });

    // 選択されたタブをアクティブに
    this.tabs[index].setAttribute('aria-selected', 'true');
    this.tabs[index].setAttribute('tabindex', '0');
    this.tabs[index].focus();
    this.panels[index].hidden = false;
  }

  handleKeydown(e, currentIndex) {
    let newIndex;

    switch (e.key) {
      case 'ArrowLeft':
        newIndex = currentIndex - 1;
        if (newIndex < 0) newIndex = this.tabs.length - 1;
        break;
      case 'ArrowRight':
        newIndex = currentIndex + 1;
        if (newIndex >= this.tabs.length) newIndex = 0;
        break;
      case 'Home':
        newIndex = 0;
        break;
      case 'End':
        newIndex = this.tabs.length - 1;
        break;
      default:
        return;
    }

    e.preventDefault();
    this.selectTab(newIndex);
  }
}
```

## チェックリスト

### 開発時の確認項目

- [ ] すべての画像に適切な代替テキストが設定されているか
- [ ] 見出しレベルが適切に構造化されているか
- [ ] キーボードのみで全ての機能が操作できるか
- [ ] フォーカスインジケーターが視認できるか
- [ ] フォームのラベルが適切に関連付けられているか
- [ ] エラーメッセージが明確でスクリーンリーダーで読み上げられるか
- [ ] コントラスト比が4.5:1以上確保されているか
- [ ] リンクテキストが文脈から独立して理解できるか
- [ ] 時間制限がある機能に延長オプションがあるか
- [ ] 動的コンテンツの変更がスクリーンリーダーに伝わるか

### テストツール

1. **WAVE** - ブラウザ拡張機能
2. **axe DevTools** - Chrome/Firefox拡張機能
3. **スクリーンリーダー**: NVDA (Windows) / VoiceOver (Mac)
4. **キーボードナビゲーション**: Tabキーのみでの操作確認

## 参考リソース

- [JIS X 8341-3:2016 達成基準チェックリスト](https://waic.jp/docs/jis2016/test-guidelines/202012/)
- [WCAG 2.1 日本語訳](https://waic.jp/docs/WCAG21/)
- [WordPress Accessibility Handbook](https://make.wordpress.org/accessibility/handbook/)
