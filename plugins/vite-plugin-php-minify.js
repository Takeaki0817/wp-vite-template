import fs from 'fs/promises';
import path from 'path';

/**
 * Vite plugin to minify PHP files by removing comments and unnecessary whitespace
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
    apply: 'build', // Only run during build, not dev
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

      // Read source file
      const content = await fs.readFile(filePath, 'utf-8');
      const originalSize = Buffer.byteLength(content, 'utf-8');

      // Minify PHP content
      const minifiedContent = minifyPhp(content, options);
      const minifiedSize = Buffer.byteLength(minifiedContent, 'utf-8');

      // Ensure output directory exists
      const outputDir = path.dirname(outputPath);
      await fs.mkdir(outputDir, { recursive: true });

      // Write minified file
      await fs.writeFile(outputPath, minifiedContent, 'utf-8');

      totalOriginalSize += originalSize;
      totalMinifiedSize += minifiedSize;
      processedCount++;
    })
  );

  // Log compression statistics
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

function minifyPhp(content, options) {
  let minified = content;

  // Remove PHP block comments /* ... */ but preserve important ones
  if (!options.preserveBlockComments) {
    minified = minified.replace(/\/\*(?!\*!)([\s\S]*?)\*\//g, '');
  }

  // Remove HTML comments <!-- ... --> but preserve conditional comments
  minified = minified.replace(/<!--(?!\[if|\s*\[endif)[\s\S]*?-->/g, '');

  // Remove excessive whitespace but preserve necessary spacing
  minified = minified.replace(/\n\s*\n/g, '\n'); // Remove empty lines
  minified = minified.replace(/^\s+/gm, ''); // Remove leading whitespace
  minified = minified.replace(/\s+$/gm, ''); // Remove trailing whitespace

  // Preserve necessary spacing around PHP tags and operators
  minified = minified.replace(/\s*<\?php\s*/g, '<?php ');
  minified = minified.replace(/\s*\?>\s*/g, '?>');

  return minified;
}

function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}
