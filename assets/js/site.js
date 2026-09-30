(() => {
  const root = document.documentElement;
  const toggle = document.getElementById('theme-toggle');
  const updateThemeLabel = () => {
    const label = root.dataset.theme === 'dark' ? '切换到浅色主题' : '切换到深色主题';
    toggle?.setAttribute('aria-label', label);
    toggle?.setAttribute('title', `${label} (Alt + T)`);
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', root.dataset.theme === 'dark' ? '#111315' : '#f8f9f7');
  };
  updateThemeLabel();
  toggle?.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('pref-theme', root.dataset.theme); } catch (_) { /* Theme still works when storage is unavailable. */ }
    updateThemeLabel();
  });

  const menu = document.querySelector('.mobile-menu');
  menu?.addEventListener('click', (event) => {
    if (event.target.closest('a')) menu.open = false;
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu?.open) {
      menu.open = false;
      menu.querySelector('summary').focus();
    }
  });
  document.addEventListener('click', (event) => {
    if (menu?.open && !menu.contains(event.target)) menu.open = false;
  });

  // Keep hash links native: focus, browser history and reduced motion all work.
  const topLink = document.getElementById('top-link');
  const updateTopLink = () => topLink?.classList.toggle('hidden', window.scrollY < window.innerHeight);
  window.addEventListener('scroll', updateTopLink, { passive: true });
  updateTopLink();

  document.querySelectorAll('pre > code').forEach((code) => {
    const pre = code.parentElement;
    const container = pre.closest('.highlight') || pre;
    if (container.querySelector('.copy-code')) return;
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'copy-code';
    button.textContent = '复制';
    button.setAttribute('aria-label', '复制代码');
    button.setAttribute('aria-live', 'polite');
    button.addEventListener('click', async () => {
      const copy = code.cloneNode(true);
      copy.querySelectorAll('.ln, .lnt, .lntd:first-child').forEach((number) => number.remove());
      try {
        await navigator.clipboard.writeText(copy.textContent);
        button.textContent = '已复制';
      } catch (_) {
        button.textContent = '请选中代码复制';
      }
      window.setTimeout(() => { button.textContent = '复制'; }, 2000);
    });
    container.appendChild(button);
  });
})();
