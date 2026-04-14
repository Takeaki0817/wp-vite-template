#!/usr/bin/env node

/**
 * WordPress テーマ用 PHP テンプレートフォーマッター
 *
 * Prettier の前後に処理を挟み、PHP/HTML 混在ファイルを安全に整形する。
 *
 * 処理方式:
 * - <?php ... ?> / <?= ... ?> をプレースホルダに退避してから HTML を Prettier で整形
 * - PHP ブロック内部は parser:php で個別に整形
 * - 閉じタグがない純粋 PHP ファイルは parser:php でファイル全体を整形
 * - <!DOCTYPE>, <html>, <head>, <body> はフラグメント対応のため退避
 * - Tailwind クラスソートは HTML 属性内で引き続き動作
 *
 * 使い方:
 *   node scripts/format-wp.mjs                    # 全 PHP ファイルを整形
 *   node scripts/format-wp.mjs --check            # 整形が必要なファイルを表示（変更しない）
 *   node scripts/format-wp.mjs --file path/to.php # 指定ファイルのみ整形
 */

import fs from 'fs/promises';
import path from 'path';
import * as prettier from 'prettier';
import glob from 'fast-glob';

const TEMPLATE_DIR = 'src/public';

async function main() {
  const check = process.argv.includes('--check');
  const fileIdx = process.argv.indexOf('--file');
  const files =
    fileIdx !== -1 && process.argv[fileIdx + 1]
      ? [process.argv[fileIdx + 1]]
      : await glob(`${TEMPLATE_DIR}/**/*.php`);

  let changed = 0;
  let errors = 0;

  for (const file of files) {
    try {
      const content = await fs.readFile(file, 'utf-8');
      const formatted = isPurePhpFile(content)
        ? await formatPurePhp(content, file)
        : await formatWpTemplate(content, file);

      if (content !== formatted) {
        if (check) {
          console.log(`  needs formatting: ${file}`);
          changed++;
        } else {
          await fs.writeFile(file, formatted, 'utf-8');
          console.log(`  formatted: ${file}`);
          changed++;
        }
      }
    } catch (e) {
      console.error(`  error: ${file} — ${e.message}`);
      errors++;
    }
  }

  const total = check ? changed + errors : changed;
  console.log(
    `\n[format-wp] ${check ? 'Check' : 'Done'}: ${total} file(s) ${check ? 'need formatting' : 'formatted'}${errors ? `, ${errors} error(s)` : ''}`
  );

  if (check && changed > 0) process.exit(1);
  if (errors > 0) process.exit(1);
}

// ---------------------------------------------------------------------------
// 判定
// ---------------------------------------------------------------------------

/**
 * 閉じタグ ?> がないファイルを純粋 PHP と判定
 */
function isPurePhpFile(content) {
  const trimmed = content.trim();
  if (!trimmed.startsWith('<?php')) return false;
  return !trimmed.includes('?>');
}

// ---------------------------------------------------------------------------
// 純粋 PHP 整形
// ---------------------------------------------------------------------------

/**
 * ファイル全体を parser:php で整形
 */
async function formatPurePhp(content, filepath) {
  const config = await prettier.resolveConfig(filepath);
  try {
    return await prettier.format(content, {
      ...config,
      parser: 'php',
      filepath,
    });
  } catch {
    // PHP 整形に失敗した場合は元のまま返す
    return content;
  }
}

// ---------------------------------------------------------------------------
// テンプレート（PHP/HTML 混在）整形
// ---------------------------------------------------------------------------

/**
 * WordPress テンプレートを整形するメイン処理
 */
async function formatWpTemplate(content, filepath) {
  // Step 1: PHP ブロックをプレースホルダに退避
  const { text: withoutPhp, blocks: phpBlocks } = extractPhpBlocks(content);

  // Step 2: ドキュメント構造タグを退避
  const { text: withoutDoc, blocks: docBlocks } = extractDocTags(withoutPhp);

  // Step 3: Prettier で HTML 整形（Tailwind クラスソート含む）
  const htmlFormatted = await formatHtml(withoutDoc, filepath);

  // Step 4: ドキュメント構造タグを復元
  const withDoc = restoreBlocks(htmlFormatted, docBlocks, 'DOC');

  // Step 5: PHP ブロックを復元（個別 PHP 整形 + インデント調整）
  const result = await restorePhpBlocks(withDoc, phpBlocks, filepath);

  return result;
}

/**
 * <?php ... ?> と <?= ... ?> をプレースホルダに退避
 */
function extractPhpBlocks(content) {
  const blocks = [];
  const text = content.replace(/<\?(?:php|=)[\s\S]*?\?>/g, (match) => {
    const id = blocks.length;
    blocks.push(match);
    return `<!--__PHP_${id}__-->`;
  });
  return { text, blocks };
}

/**
 * <!DOCTYPE>, <html>, </html>, <head>, </head>, <body>, </body> を退避
 */
function extractDocTags(content) {
  const blocks = [];
  const text = content.replace(
    /<!DOCTYPE[^>]*>|<\/?\s*(?:html|head|body)(?:\s[^>]*)?\s*>/gi,
    (match) => {
      const id = blocks.length;
      blocks.push(match);
      return `<!--__DOC_${id}__-->`;
    }
  );
  return { text, blocks };
}

/**
 * プレースホルダ付き HTML を Prettier で整形
 */
async function formatHtml(content, filepath) {
  const config = await prettier.resolveConfig(filepath);
  try {
    return await prettier.format(content, {
      ...config,
      parser: 'html',
      filepath: filepath.replace(/\.php$/, '.html'), // HTML として処理させる
      htmlWhitespaceSensitivity: 'ignore',
    });
  } catch {
    // HTML 整形に失敗した場合はそのまま返す
    return content;
  }
}

/**
 * DOC プレースホルダを復元
 */
function restoreBlocks(content, blocks, prefix) {
  return content.replace(
    new RegExp(`([ \\t]*)<!--__${prefix}_(\\d+)__-->`, 'g'),
    (_, indent, id) => indent + blocks[parseInt(id)]
  );
}

/**
 * PHP プレースホルダを復元（個別 PHP 整形 + インデント調整）
 */
async function restorePhpBlocks(content, blocks, filepath) {
  const config = await prettier.resolveConfig(filepath);

  // 全プレースホルダの位置を収集（非同期処理のため先に集める）
  const replacements = [];
  const pattern = /([ \t]*)<!--__PHP_(\d+)__-->/g;
  let match;
  while ((match = pattern.exec(content)) !== null) {
    replacements.push({
      fullMatch: match[0],
      indent: match[1],
      id: parseInt(match[2]),
      index: match.index,
    });
  }

  // 各 PHP ブロックを整形
  let result = content;
  // 後ろから置換（インデックスがずれないように）
  for (let i = replacements.length - 1; i >= 0; i--) {
    const { fullMatch, indent, id, index } = replacements[i];
    const original = blocks[id];
    const formatted = await formatPhpBlock(original, config);
    const reindented = reindentBlock(formatted, indent);

    result =
      result.slice(0, index) +
      reindented +
      result.slice(index + fullMatch.length);
  }

  return result;
}

/**
 * 単一の PHP ブロックを parser:php で整形
 *
 * - <?= ... ?> は短いため整形しない
 * - 整形失敗時は元のブロックをそのまま返す
 */
async function formatPhpBlock(block, config) {
  // <?= ... ?> は整形しない
  if (block.trimStart().startsWith('<?=')) return block;

  try {
    let formatted = await prettier.format(block, {
      ...config,
      parser: 'php',
    });
    // Prettier が末尾に追加する改行を除去
    formatted = formatted.replace(/\n+$/, '');
    return formatted;
  } catch {
    return block;
  }
}

/**
 * 複数行ブロックを指定インデントに揃える
 */
function reindentBlock(block, indent) {
  const lines = block.split('\n');
  if (lines.length <= 1) return indent + block.trim();

  // 2 行目以降の最小インデントを検出
  const indents = lines
    .slice(1)
    .filter((l) => l.trim().length > 0)
    .map((l) => l.match(/^(\s*)/)[1].length);
  const minIndent = indents.length > 0 ? Math.min(...indents) : 0;

  return lines
    .map((line, i) => {
      if (i === 0) return indent + line.trim();
      if (line.trim().length === 0) return '';
      return indent + line.slice(minIndent);
    })
    .join('\n');
}

// ---------------------------------------------------------------------------

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
