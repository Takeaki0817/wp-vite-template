<?php
/**
 * グローバルサイト設定
 * 
 * プロジェクトに合わせてこれらの値をカスタマイズしてください
 */

$site_config = [
  'company' => [
    'name' => 'Your Company Name',
    'tagline' => 'Your Company Tagline',
    'address' => '〒000-0000 Your Address',
    'city' => 'Your City',
    'phone' => '000-0000-0000',
    'email' => 'info@yourcompany.com',
    'website' => 'https://yourcompany.com',
    'business_hours' => [
      'weekdays' => '9:00～18:00',
      'saturday' => '9:00～12:00',
      'sunday' => 'Closed',
    ],
  ],
  
  'social' => [
    'twitter' => 'https://twitter.com/yourcompany',
    'facebook' => 'https://facebook.com/yourcompany',
    'instagram' => 'https://instagram.com/yourcompany',
    'linkedin' => 'https://linkedin.com/company/yourcompany',
  ],
  
  'features' => [
    'show_social_links' => true,
    'show_business_hours' => true,
    'show_contact_info' => true,
  ],
];

// 設定をグローバルに利用可能にする
$GLOBALS['site_config'] = $site_config;