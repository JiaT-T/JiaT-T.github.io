(() => {
  const hero = document.querySelector('.home-hero');
  if (!hero) return;
  document.body.classList.add('scene-enhanced');

  // Keep the floating header readable once the scene leaves the viewport.
  const header = document.querySelector('.header');
  if (header) {
    new IntersectionObserver(([entry]) => {
      header.classList.toggle('is-scrolled', !entry.isIntersecting);
    }, { rootMargin: '-80px 0px 0px 0px', threshold: 0 }).observe(hero);
  }

  const visuals = hero.querySelector('.hero-visuals');
  const arrows = [...hero.querySelectorAll('.scene-arrow')];
  if (!visuals || !arrows.length) return;

  // Only the selected picture is loaded; the other templates stay inert.
  const scenes = [...visuals.querySelectorAll('[data-scene-image], [data-scene-template]')].map((source) => ({
    id: source.dataset.sceneImage || source.dataset.sceneTemplate,
    source,
    frame: source.matches('template') ? null : source,
  }));
  if (scenes.length < 2) return;

  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const status = hero.querySelector('.scene-status');
  const error = hero.querySelector('.scene-error');
  const playback = hero.querySelector('.scene-playback');
  const playbackLabel = playback?.querySelector('span');
  const rotationDelay = 8000;
  const fadeDuration = 400;
  let currentIndex = -1;
  let remaining = scenes.map((_, index) => index);
  let busy = false;
  let paused = false;
  let heroVisible = true;
  let controlFocused = false;
  let rotationTimer;
  arrows.forEach((arrow) => { arrow.hidden = false; });

  const chooseScene = (excludedIndex = currentIndex) => {
    let choices = remaining.filter((index) => index !== excludedIndex);
    if (!choices.length) {
      remaining = scenes.map((_, index) => index);
      choices = remaining.filter((index) => index !== excludedIndex);
    }
    const selected = choices[Math.floor(Math.random() * choices.length)];
    remaining = remaining.filter((index) => index !== selected);
    return selected;
  };

  const canRotate = () => !paused && !reducedMotion.matches && !document.hidden && heroVisible && !controlFocused;
  const scheduleRotation = () => {
    clearTimeout(rotationTimer);
    if (currentIndex < 0 || busy || !canRotate()) return;
    rotationTimer = setTimeout(() => showScene(chooseScene(), 'auto'), rotationDelay);
  };

  const updatePlayback = () => {
    if (!playback) return;
    playback.hidden = reducedMotion.matches;
    playback.setAttribute('aria-pressed', String(paused));
    playback.setAttribute('aria-label', paused ? '继续自动轮换背景' : '暂停自动轮换背景');
    if (playbackLabel) playbackLabel.textContent = paused ? '继续轮换' : '暂停轮换';
  };

  const announceScene = () => {
    const scene = scenes[currentIndex];
    if (status) status.textContent = `背景：${scene.frame?.dataset.sceneName || scene.id}，第 ${currentIndex + 1} 张，共 ${scenes.length} 张。`;
  };

  const showScene = async (nextIndex, reason) => {
    if (busy) return;
    const next = scenes[nextIndex];
    busy = true;
    clearTimeout(rotationTimer);
    arrows.forEach((arrow) => arrow.setAttribute('aria-disabled', 'true'));
    if (status && reason === 'manual') status.setAttribute('aria-busy', 'true');
    if (error) error.hidden = true;
    let timeout;
    try {
      if (!next.frame) {
        next.frame = next.source.content.firstElementChild.cloneNode(true);
        const image = next.frame.querySelector('img');
        if (image) {
          image.loading = 'eager';
          if (currentIndex < 0) image.fetchPriority = 'high';
        }
        visuals.append(next.frame);
      }
      const image = next.frame.querySelector('img');
      if (!image) throw new Error('Image unavailable');
      await Promise.race([
        image.decode(),
        new Promise((_, reject) => { timeout = setTimeout(() => reject(new Error('Image timeout')), 15000); }),
      ]);
      if (!image.naturalWidth) throw new Error('Image unavailable');
      if (reason === 'auto' && !canRotate()) return;
      const previous = scenes[currentIndex];
      next.frame.hidden = false;
      next.frame.style.zIndex = '1';
      // Paint the decoded frame at zero opacity before starting its fade.
      await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
      if (reason === 'auto' && !canRotate()) {
        next.frame.hidden = true;
        next.frame.style.removeProperty('z-index');
        return;
      }
      next.frame.classList.add('is-active');
      hero.dataset.scene = next.id;
      currentIndex = nextIndex;
      try { sessionStorage.setItem('last-home-scene', next.id); } catch (_) { /* Storage is optional. */ }
      if (reason !== 'auto') announceScene();
      if (!reducedMotion.matches) await new Promise((resolve) => setTimeout(resolve, fadeDuration));
      // Keep the old picture opaque underneath the fade, avoiding a dark flash.
      if (previous && previous !== next) {
        previous.frame.hidden = true;
        previous.frame.classList.remove('is-active');
      }
      next.frame.style.removeProperty('z-index');
    } catch (_) {
      // A failed load must never replace the picture already on screen.
      if (next.frame && nextIndex !== currentIndex && next.source.matches('template')) {
        next.frame.remove();
        next.frame = null;
      }
      if (reason !== 'auto') {
        if (error) error.hidden = false;
        if (status) status.textContent = error?.textContent || '背景加载暂时失败，请重试。';
      }
    } finally {
      clearTimeout(timeout);
      busy = false;
      arrows.forEach((arrow) => arrow.removeAttribute('aria-disabled'));
      status?.removeAttribute('aria-busy');
      scheduleRotation();
    }
  };

  arrows.forEach((arrow) => {
    arrow.addEventListener('click', () => {
      if (!busy) showScene(chooseScene(), 'manual');
    });
    arrow.addEventListener('focus', () => {
      controlFocused = arrow.matches(':focus-visible');
      scheduleRotation();
    });
    arrow.addEventListener('blur', (event) => {
      if (!arrows.includes(event.relatedTarget)) controlFocused = false;
      scheduleRotation();
    });
    arrow.addEventListener('keydown', (event) => {
      if (!['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
      event.preventDefault();
      controlFocused = true;
      const step = event.key === 'ArrowLeft' ? -1 : 1;
      arrows.find((item) => Number(item.dataset.sceneStep) === step)?.focus();
      if (!busy) showScene(chooseScene(), 'manual');
    });
  });

  playback?.addEventListener('click', () => {
    paused = !paused;
    updatePlayback();
    scheduleRotation();
  });
  document.addEventListener('visibilitychange', scheduleRotation);
  reducedMotion.addEventListener('change', () => {
    updatePlayback();
    scheduleRotation();
  });
  new IntersectionObserver(([entry]) => {
    heroVisible = entry.isIntersecting;
    scheduleRotation();
  }, { threshold: 0.05 }).observe(hero);
  window.addEventListener('pagehide', () => clearTimeout(rotationTimer));
  window.addEventListener('pageshow', (event) => {
    if (event.persisted && !busy) showScene(chooseScene(), 'initial');
  });

  updatePlayback();
  let lastIndex = -1;
  try { lastIndex = scenes.findIndex((scene) => scene.id === sessionStorage.getItem('last-home-scene')); } catch (_) { /* Storage is optional. */ }
  const start = async () => {
    // Try another scene if the first random image cannot be loaded.
    for (let attempt = 0; attempt < scenes.length && currentIndex < 0; attempt += 1) {
      await showScene(chooseScene(attempt === 0 ? lastIndex : -1), 'initial');
    }
  };
  start();
})();
