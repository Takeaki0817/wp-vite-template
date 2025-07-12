// vite-plugin-sharp.js
import { promises as fs } from 'fs';
import path from 'path';
import sharp from 'sharp';
import fg from 'fast-glob';
import crypto from 'crypto';
import { optimize } from 'svgo';

export default function vitePluginSharp(options = {}) {
  const {
    srcDir = 'src',
    outDir = 'dist',
    imageExtensions = ['jpg', 'jpeg', 'png', 'gif', 'svg'],
    avifOptions = { quality: 50 },
    webpOptions = { quality: 80 },
    compressOptions = {
      jpg: { quality: 80 },
      jpeg: { quality: 80 },
      png: { compressionLevel: 8 },
      webp: { quality: 80 },
    },
    resizeOptions = {
      widthRatio: 0.5,
      heightRatio: 0.5,
    },
  } = options;

  const cacheFilePath = path.resolve(outDir, '.sharp-cache.json');
  const timestampFilePath = path.resolve('.last-image-process-time');
  let imageCache = new Map();
  let lastProcessTime = 0;
  let isWatching = false;

  // ファイルのハッシュを計算
  async function getFileHash(filePath) {
    const content = await fs.readFile(filePath);
    return crypto.createHash('md5').update(content).digest('hex');
  }

  // 画像ディレクトリの変更をチェック
  async function hasImageChanges() {
    const pattern = `${srcDir}/**/*.{${imageExtensions.join(',')}}`;
    const files = await fg(pattern);
    
    // タイムスタンプファイルから最終処理時刻を読み込み
    try {
      const timestamp = await fs.readFile(timestampFilePath, 'utf-8');
      lastProcessTime = parseInt(timestamp, 10);
    } catch {
      // ファイルがない場合は初回実行
      console.log('[vite-plugin-sharp] First build detected - processing all images');
      return true;
    }

    // 各ファイルの更新時刻をチェック
    for (const file of files) {
      const stats = await fs.stat(file);
      if (stats.mtimeMs > lastProcessTime) {
        console.log(`[vite-plugin-sharp] Image changed: ${file}`);
        return true;
      }
    }

    return false;
  }

  // タイムスタンプを更新
  async function updateTimestamp() {
    await fs.writeFile(timestampFilePath, Date.now().toString());
  }

  // 画像処理の本体
  async function processImages(shouldForce = false) {
    const hasChanges = shouldForce || await hasImageChanges();
    
    if (!hasChanges) {
      console.log('[vite-plugin-sharp] No image changes detected - skipping processing');
      return;
    }

    console.log('[vite-plugin-sharp] Processing images...');
    
    // キャッシュファイルの読み込み
    let cache = {};
    try {
      const cacheContent = await fs.readFile(cacheFilePath, 'utf-8');
      cache = JSON.parse(cacheContent);
    } catch {
      cache = {};
    }

    const pattern = `${srcDir}/**/*.{${imageExtensions.join(',')}}`;
    const files = await fg(pattern);

    for (const file of files) {
      // 相対パスを取得
      const relativePath = path.relative(srcDir, file);
      const outputPath = path.join(outDir, relativePath);
      const outputDir = path.dirname(outputPath);

      // 出力ディレクトリを作成
      await fs.mkdir(outputDir, { recursive: true });

      // ファイルハッシュを計算
      const currentHash = await getFileHash(file);

      // キャッシュと比較
      if (cache[relativePath] === currentHash) {
        // ファイルが存在するか確認
        try {
          await fs.access(outputPath);
          const ext = path.extname(file).toLowerCase();
          if (ext !== '.svg') {
            const baseName = path.basename(file, ext);
            const baseDir = path.dirname(outputPath);
            // 生成ファイルの存在確認
            await fs.access(path.join(baseDir, `${baseName}@1x.webp`));
            await fs.access(path.join(baseDir, `${baseName}@1x.avif`));
          }
          continue; // スキップ
        } catch {
          // ファイルが存在しない場合は処理を続行
        }
      }

      console.log(`[vite-plugin-sharp] Processing: ${relativePath}`);
      const ext = path.extname(file).toLowerCase();

      if (ext === '.svg') {
        // SVG最適化
        const svgContent = await fs.readFile(file, 'utf-8');
        const result = optimize(svgContent, {
          path: file,
          multipass: true,
          plugins: [
            {
              name: 'preset-default',
              params: {
                overrides: {
                  removeViewBox: false,
                  cleanupIds: false,
                },
              },
            },
          ],
        });
        await fs.writeFile(outputPath, result.data);
      } else {
        // 画像処理（既存のロジック）
        const image = sharp(file);
        const metadata = await image.metadata();
        const baseName = path.basename(file, ext);
        const baseDir = path.dirname(outputPath);

        // @1x（元サイズ）の処理
        const format = ext.slice(1);
        const compressOption = compressOptions[format] || {};
        
        if (format === 'jpg' || format === 'jpeg') {
          await image.clone().jpeg(compressOption).toFile(path.join(baseDir, `${baseName}@1x${ext}`));
        } else if (format === 'png') {
          await image.clone().png(compressOption).toFile(path.join(baseDir, `${baseName}@1x${ext}`));
        } else {
          await image.clone().toFile(path.join(baseDir, `${baseName}@1x${ext}`));
        }

        // WebP変換
        await image.clone().webp(webpOptions).toFile(path.join(baseDir, `${baseName}@1x.webp`));

        // AVIF変換
        await image.clone().avif(avifOptions).toFile(path.join(baseDir, `${baseName}@1x.avif`));

        // @2x（半分サイズ）の処理
        const resizedWidth = Math.round(metadata.width * resizeOptions.widthRatio);
        const resizedHeight = Math.round(metadata.height * resizeOptions.heightRatio);

        if (format === 'jpg' || format === 'jpeg') {
          await image.clone().resize(resizedWidth, resizedHeight).jpeg(compressOption).toFile(path.join(baseDir, `${baseName}@2x${ext}`));
        } else if (format === 'png') {
          await image.clone().resize(resizedWidth, resizedHeight).png(compressOption).toFile(path.join(baseDir, `${baseName}@2x${ext}`));
        } else {
          await image.clone().resize(resizedWidth, resizedHeight).toFile(path.join(baseDir, `${baseName}@2x${ext}`));
        }

        await image.clone().resize(resizedWidth, resizedHeight).webp(webpOptions).toFile(path.join(baseDir, `${baseName}@2x.webp`));
        await image.clone().resize(resizedWidth, resizedHeight).avif(avifOptions).toFile(path.join(baseDir, `${baseName}@2x.avif`));
      }

      // キャッシュを更新
      cache[relativePath] = currentHash;
    }

    // キャッシュファイルを保存
    await fs.writeFile(cacheFilePath, JSON.stringify(cache, null, 2));
    
    // タイムスタンプを更新
    await updateTimestamp();
    
    console.log('[vite-plugin-sharp] Image processing completed');
  }

  return {
    name: 'vite-plugin-sharp',
    
    async buildStart() {
      // ビルド開始時に画像処理
      await processImages();
    },

    configureServer(server) {
      // 開発サーバーでファイル監視
      isWatching = true;
      
      server.watcher.add(path.join(srcDir, '**/*.{' + imageExtensions.join(',') + '}'));
      
      // 画像ファイルの変更を監視
      server.watcher.on('change', async (file) => {
        if (imageExtensions.some(ext => file.endsWith(`.${ext}`))) {
          console.log(`[vite-plugin-sharp] Image file changed: ${file}`);
          await processImages(true);
        }
      });
      
      server.watcher.on('add', async (file) => {
        if (imageExtensions.some(ext => file.endsWith(`.${ext}`))) {
          console.log(`[vite-plugin-sharp] New image added: ${file}`);
          await processImages(true);
        }
      });
    },
    
    closeBundle() {
      // watchモードでない場合のみ
      if (!isWatching) {
        console.log('[vite-plugin-sharp] Build completed');
      }
    }
  };
}