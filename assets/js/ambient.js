(() => {
    const layer = document.querySelector('.site-ambient');
    if (!layer) return;

    const syncVisibility = () => {
        layer.dataset.paused = String(document.hidden);
    };

    document.addEventListener('visibilitychange', syncVisibility);
    syncVisibility();
})();
