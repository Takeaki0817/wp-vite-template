/**
 * WordPress PHP テンプレート用 Prettier プラグイン
 *
 * .php ファイルを保存時に自動整形するための Prettier プラグイン。
 * VSCode の Format on Save で動作する。
 *
 * 動作:
 * - <?php ... ?> / <?= ... ?> を退避 → HTML を Prettier 整形 → PHP を個別整形して復元
 * - 閉じタグなし PHP は parser:php でファイル全体を整形
 * - <!DOCTYPE>, <html>, <head>, <body> はフラグメント対応のため退避
 * - Tailwind クラスソートは HTML 属性内で引き続き動作
 */

import * as prettier from 'prettier';
import { doc } from 'prettier';

const { join, hardline } = doc.builders;

// ---------------------------------------------------------------------------
// プラグイン定義
// ---------------------------------------------------------------------------

export const languages = [
  {
    name: 'WordPress PHP',
    parsers: ['wp-php'],
    extensions: ['.php'],
    vscodeLanguageIds: ['php'],
  },
];

export const parsers = {
  'wp-php': {
    async parse(text, options) {
      const body = await formatWpPhp(text, options);
      return { type: 'wp-php-root', body };
    },
    astFormat: 'wp-php-ast',
    locStart: () => 0,
    locEnd: (node) => node.body?.length ?? 0,
  },
};

export const printers = {
  'wp-php-ast': {
    print(path) {
      const node = path.getValue();
      const lines = node.body.replace(/\n$/, '').split('\n');
      return [join(hardline, lines), hardline];
    },
  },
};

// ---------------------------------------------------------------------------
// メイン処理
// ---------------------------------------------------------------------------

/**
 * PHP ファイルの種別を判定して整形
 */
async function formatWpPhp(text, options) {
  if (isPurePhpFile(text)) {
    return formatPurePhp(text, options);
  }
  return formatTemplate(text, options);
}

/**
 * 閉じタグ ?> がなければ純粋 PHP
 */
function isPurePhpFile(text) {
  const trimmed = text.trim();
  return trimmed.startsWith('<?php') && !trimmed.includes('?>');
}

/**
 * 純粋 PHP ファイルを parser:php で整形
 */
async function formatPurePhp(text, options) {
  try {
    return await prettier.format(text, {
      ...pickOptions(options),
      parser: 'php',
    });
  } catch {
    return text;
  }
}

/**
 * テンプレート（PHP/HTML 混在）を整形
 */
async function formatTemplate(text, options) {
  // Step 1: PHP ブロックを退避
  const phpBlocks = [];
  let processed = text.replace(/<\?(?:php|=)[\s\S]*?\?>/g, (match) => {
    phpBlocks.push(match);
    return `<!--__PHP_${phpBlocks.length - 1}__-->`;
  });

  // Step 2: ドキュメント構造タグを退避
  const docBlocks = [];
  processed = processed.replace(
    /<!DOCTYPE[^>]*>|<\/?\s*(?:html|head|body)(?:\s[^>]*)?\s*>/gi,
    (match) => {
      docBlocks.push(match);
      return `<!--__DOC_${docBlocks.length - 1}__-->`;
    }
  );

  // Step 3: HTML 整形（Tailwind クラスソート含む）
  let formatted;
  try {
    formatted = await prettier.format(processed, {
      ...pickOptions(options),
      parser: 'html',
      htmlWhitespaceSensitivity: 'ignore',
    });
  } catch {
    formatted = processed;
  }

  // Step 4: ドキュメント構造タグを復元
  formatted = formatted.replace(
    /([ \t]*)<!--__DOC_(\d+)__-->/g,
    (_, indent, id) => indent + docBlocks[parseInt(id)]
  );

  // Step 5: PHP ブロックを復元（個別整形 + インデント調整）
  const pattern = /([ \t]*)<!--__PHP_(\d+)__-->/g;
  const replacements = [];
  let match;
  while ((match = pattern.exec(formatted)) !== null) {
    replacements.push({
      fullMatch: match[0],
      indent: match[1],
      id: parseInt(match[2]),
      index: match.index,
    });
  }

  let result = formatted;
  for (let i = replacements.length - 1; i >= 0; i--) {
    const { fullMatch, indent, id, index } = replacements[i];
    const original = phpBlocks[id];
    const phpFormatted = await formatPhpBlock(original, options);
    const reindented = reindentBlock(phpFormatted, indent);
    result =
      result.slice(0, index) + reindented + result.slice(index + fullMatch.length);
  }

  return result;
}

// ---------------------------------------------------------------------------
// ユーティリティ
// ---------------------------------------------------------------------------

/**
 * 単一 PHP ブロックを parser:php で整形
 */
async function formatPhpBlock(block, options) {
  // <?= ... ?> は短いため整形しない
  if (block.trimStart().startsWith('<?=')) return block;

  try {
    let formatted = await prettier.format(block, {
      ...pickOptions(options),
      parser: 'php',
    });
    return formatted.replace(/\n+$/, '');
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

/**
 * 内部の prettier.format() に渡すオプションを抽出
 * （プラグイン内から再帰呼び出しする際に安全なオプションのみ渡す）
 */
function pickOptions(options) {
  return {
    tabWidth: options.tabWidth,
    useTabs: options.useTabs,
    singleQuote: options.singleQuote,
    printWidth: options.printWidth,
    trailingComma: options.trailingComma,
    plugins: options.plugins,
  };
}
