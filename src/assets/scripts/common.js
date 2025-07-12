(function () {
  document.addEventListener('DOMContentLoaded', () => {
    viewportScaleControl();
  });

  /**
   * ビューポート縮小制御
   * 360px未満の画面幅では、360pxのレイアウトを縮小表示
   */
  const viewportScaleControl = () => {
    const MIN_WIDTH = 440;
    let metaViewport = document.querySelector('meta[name="viewport"]');

    // viewportメタタグが存在しない場合は作成
    if (!metaViewport) {
      metaViewport = document.createElement('meta');
      metaViewport.name = 'viewport';
      document.head.appendChild(metaViewport);
    }

    function updateViewport() {
      const screenWidth = window.screen.width || window.innerWidth;

      if (screenWidth < MIN_WIDTH) {
        // 360px未満の場合、縮小率を計算
        const scale = screenWidth / MIN_WIDTH;
        metaViewport.content = `width=${MIN_WIDTH}, initial-scale=${scale}, minimum-scale=${scale}, maximum-scale=${scale}, user-scalable=no`;
      } else {
        // 360px以上の場合、通常のレスポンシブ表示
        metaViewport.content =
          'width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=5';
      }
    }

    // 初期実行
    updateViewport();

    // orientationchangeイベントでも更新（画面回転時）
    window.addEventListener('orientationchange', function () {
      setTimeout(updateViewport, 100); // 回転アニメーション完了を待つ
    });

    // ページ表示時にも念のため実行
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', updateViewport);
    }
  };
})();
