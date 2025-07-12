import fs from 'fs';
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
    writeBundle() {
      minifyPhpFiles(srcDir, outDir, {
        preserveLineComments,
        preserveBlockComments,
      });
    },
  };
}

function minifyPhpFiles(srcDir, outDir, options) {
  const phpFiles = findPhpFiles(srcDir);

  phpFiles.forEach((filePath) => {
    const relativePath = path.relative(srcDir, filePath);
    const outputPath = path.join(outDir, relativePath);

    // Read source file
    const content = fs.readFileSync(filePath, 'utf-8');

    // Minify PHP content
    const minifiedContent = minifyPhp(content, options);

    // Ensure output directory exists
    const outputDir = path.dirname(outputPath);
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    // Write minified file
    fs.writeFileSync(outputPath, minifiedContent, 'utf-8');

    // console.log(`Minified PHP: ${relativePath}`);
  });
}

function findPhpFiles(dir) {
  const files = [];

  function scanDir(currentDir) {
    const items = fs.readdirSync(currentDir);

    items.forEach((item) => {
      const itemPath = path.join(currentDir, item);
      const stat = fs.statSync(itemPath);

      if (stat.isDirectory()) {
        scanDir(itemPath);
      } else if (item.endsWith('.php')) {
        files.push(itemPath);
      }
    });
  }

  scanDir(dir);
  return files;
}

function minifyPhp(content, options) {
  let minified = content;

  // Remove PHP line comments (// and #) but preserve URLs and important comments
  // if (!options.preserveLineComments) {
  //   minified = minified.replace(
  //     /(?<!:)\/\/(?![^\r\n]*?(?:https?:|ftp:)).*$/gm,
  //     '',
  //   );
  //   minified = minified.replace(
  //     /(?<!:)#(?![^\r\n]*?(?:https?:|ftp:)).*$/gm,
  //     '',
  //   );
  // }

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
