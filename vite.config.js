import { defineConfig } from 'vite';
import path from 'path';
import glob from 'fast-glob';
import vitePluginSharp from './plugins/vite-plugin-sharp';
import vitePluginPhpMinify from './plugins/vite-plugin-php-minify';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  root: path.resolve(__dirname),
  base: './',
  publicDir: path.resolve(__dirname, 'src/public'),
  build: {
    outDir: path.resolve(__dirname, 'dist'),
    emptyOutDir: false,
    copyPublicDir: true,
    assetsDir: '',
    minify: 'esbuild',
    manifest: true,
    watch:
      process.env.NODE_ENV === 'development'
        ? {
            include: ['src/assets/**', 'src/public/**'],
          }
        : null,
    esbuild: {
      drop: ['console', 'debugger'],
      minifyWhitespace: true,
      minifyIdentifiers: true,
      minifySyntax: true,
    },
    rollupOptions: {
      // src内のすべてのJSおよびCSSファイルを動的にインクルード
      input: glob.sync('src/assets/**/*.{js,css}'),
      preserveEntrySignatures: 'strict',
      output: {
        dir: path.resolve(__dirname, 'dist'),
        preserveModules: true, // モジュールを保持
        preserveModulesRoot: 'src', // モジュールのルートをsrcに設定
        entryFileNames: '[name].js', // エントリーポイントのファイル名を元の名前に
        chunkFileNames: '[name].js', // チャンクファイルの名前を元の名前に
        assetFileNames: '[name][extname]', // アセットファイルの名前を元の名前に
      },
    },
  },
  plugins: [
    vitePluginSharp({
      srcDir: 'src/assets/images',
      outDir: 'dist/assets/images',
      imageExtensions: ['jpg', 'jpeg', 'png', 'gif', 'svg'],
      avifOptions: {
        quality: 50,
      },
      webpOptions: {
        quality: 80,
      },
      compressOptions: {
        jpg: { quality: 80 },
        png: { compressionLevel: 8 },
        webp: { quality: 80 },
      },
    }),
    vitePluginPhpMinify({
      srcDir: 'src/public',
      outDir: 'dist',
      preserveLineComments: false,
      preserveBlockComments: false,
    }),
    tailwindcss({
      content: ['./src/public/**/*.php', './src/public/**/*.html'],
    }),
  ],
});
