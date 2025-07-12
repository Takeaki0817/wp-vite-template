<?php
/**
 * メインテーマ関数
 *
 * @package WordPressViteTemplate
 * @version 1.0.0
 */

// 直接アクセスを防止
if (!defined('ABSPATH')) {
  exit();
}

// キャッシュバスティング用テーマバージョン
define('THEME_VERSION', '1.0.0');

// テーマディレクトリ定数
define('THEME_URI', get_template_directory_uri());
define('THEME_PATH', get_template_directory());
define('THEME_ASSETS_URI', THEME_URI . '/assets');

// テーマモジュールを読み込み
$functions_dir = THEME_PATH . '/functions/';

// コアテーマモジュール（読み込み順）
$modules = [
  'theme-setup.php',
  'security.php',
  'performance.php',
  'media-optimization.php',
];

// グローバル変数を読み込み
$variables_dir = THEME_PATH . '/variables/';
$variables = ['global-config.php'];

foreach ($variables as $variable_file) {
  $variable_path = $variables_dir . $variable_file;

  if (file_exists($variable_path)) {
    require_once $variable_path;
  }
}

// テンプレートユーティリティ
$utils_dir = THEME_PATH . '/templates/utils/';
$utils = ['optimized-image.php', 'art-direction-image.php'];

// ユーティリティ関数を読み込み
foreach ($utils as $util) {
  $util_path = $utils_dir . $util;

  if (file_exists($util_path)) {
    require_once $util_path;
  }
}

foreach ($modules as $module) {
  $module_path = $functions_dir . $module;

  if (file_exists($module_path)) {
    require_once $module_path;
  }
}

// ナビゲーションメニューを登録
register_nav_menus([
  'primary' => __('Primary Navigation', 'text-domain'),
  'footer' => __('Footer Navigation', 'text-domain'),
]);

// テーマサポート
add_theme_support('post-thumbnails');
add_theme_support('title-tag');
add_theme_support('html5', ['search-form', 'comment-form', 'comment-list', 'gallery', 'caption']);