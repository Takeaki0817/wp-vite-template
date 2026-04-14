import fs from 'fs/promises';
import path from 'path';

/**
 * PHP ファイルからコメント・不要な空白を除去する Vite プラグイン
 */
export default function vitePluginPhpMinify(options = {}) {
  const {
    srcDir = 'src/public',
    outDir = 'dist',
    preserveLineComments = false,
    preserveBlockComments = false,
  } = options;

  return {
    name: 'vite-plugin-php-minify',
    apply: 'build', // 本番ビルド時のみ実行
    async writeBundle() {
      await minifyPhpFiles(srcDir, outDir, {
        preserveLineComments,
        preserveBlockComments,
      });
    },
  };
}

async function minifyPhpFiles(srcDir, outDir, options) {
  const phpFiles = await findPhpFiles(srcDir);

  let totalOriginalSize = 0;
  let totalMinifiedSize = 0;
  let processedCount = 0;

  await Promise.all(
    phpFiles.map(async (filePath) => {
      const relativePath = path.relative(srcDir, filePath);
      const outputPath = path.join(outDir, relativePath);

      // ソースファイルを読み込み
      const content = await fs.readFile(filePath, 'utf-8');
      const originalSize = Buffer.byteLength(content, 'utf-8');

      // PHP を圧縮
      const minifiedContent = minifyPhp(content, options);
      const minifiedSize = Buffer.byteLength(minifiedContent, 'utf-8');

      // 出力先ディレクトリを作成
      const outputDir = path.dirname(outputPath);
      await fs.mkdir(outputDir, { recursive: true });

      // 圧縮済みファイルを書き出し
      await fs.writeFile(outputPath, minifiedContent, 'utf-8');

      totalOriginalSize += originalSize;
      totalMinifiedSize += minifiedSize;
      processedCount++;
    })
  );

  // 圧縮統計をログ出力
  const savedBytes = totalOriginalSize - totalMinifiedSize;
  const reductionPercent =
    totalOriginalSize > 0
      ? ((savedBytes / totalOriginalSize) * 100).toFixed(2)
      : 0;

  console.log('\n[vite-plugin-php-minify] Compression Statistics:');
  console.log(`  Files processed: ${processedCount}`);
  console.log(
    `  Original size:   ${formatBytes(totalOriginalSize)}`
  );
  console.log(
    `  Minified size:   ${formatBytes(totalMinifiedSize)}`
  );
  console.log(
    `  Saved:           ${formatBytes(savedBytes)} (${reductionPercent}%)\n`
  );
}

/**
 * 指定ディレクトリ以下の .php ファイルを再帰的に検索
 */
async function findPhpFiles(dir) {
  const files = [];

  async function scanDir(currentDir) {
    try {
      await fs.access(currentDir);
    } catch {
      return;
    }

    const items = await fs.readdir(currentDir);

    await Promise.all(
      items.map(async (item) => {
        const itemPath = path.join(currentDir, item);
        const stat = await fs.stat(itemPath);

        if (stat.isDirectory()) {
          await scanDir(itemPath);
        } else if (item.endsWith('.php')) {
          files.push(itemPath);
        }
      })
    );
  }

  await scanDir(dir);
  return files;
}

/**
 * PHP ソースを圧縮する
 *
 * 処理手順:
 * 1. 文字列リテラルをプレースホルダに退避（誤削除を防止）
 * 2. コメント・空白を削除
 * 3. 文字列リテラルを復元
 */
function minifyPhp(content, options) {
  // 文字列リテラル（'...' / "..." / ヒアドキュメント / Nowdoc）を
  // プレースホルダに退避し、コメント・空白削除の誤マッチを防ぐ
  const strings = [];
  let safed = content.replace(
    /<<<['"]?(\w+)['"]?\r?\n[\s\S]*?\r?\n\s*\1;|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'/g,
    (match) => {
      strings.push(match);
      return `\x00STR${strings.length - 1}\x00`;
    }
  );

  // PHP ブロックコメント削除（/*! で始まる重要コメントは保持）
  if (!options.preserveBlockComments) {
    safed = safed.replace(/\/\*(?!\*!)([\s\S]*?)\*\//g, '');
  }

  // HTML コメント削除（IE 条件付きコメントは保持）
  safed = safed.replace(/<!--(?!\[if|\s*\[endif)[\s\S]*?-->/g, '');

  // 空行を削除
  safed = safed.replace(/\n\s*\n/g, '\n');

  // 行末の空白を削除（行頭空白は複数行文字列やインデントを壊すため削除しない）
  safed = safed.replace(/\s+$/gm, '');

  // 文字列リテラルを復元
  safed = safed.replace(/\x00STR(\d+)\x00/g, (_, i) => strings[parseInt(i)]);

  return safed;
}

/**
 * バイト数を人間が読みやすい形式に変換
 */
function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}
