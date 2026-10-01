(() => {
  const hero = document.querySelector('.home-hero');
  if (!hero) return;
  document.body.classList.add('scene-enhanced');
  const picker = hero.querySelector('.scene-picker');
  const visuals = hero.querySelector('.hero-visuals');
  const buttons = [...picker.querySelectorAll('button')];
  const motionToggle = hero.querySelector('.motion-toggle');
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const narrow = matchMedia('(max-width: 600px)');
  const error = hero.querySelector('.scene-error');
  let savedMotion;
  try { savedMotion = localStorage.getItem('hero-motion'); } catch (_) { /* Optional preference. */ }
  let motionEnabled = !reducedMotion.matches && !navigator.connection?.saveData && savedMotion !== 'paused';
  let posterReady = false;
  let inView = false;
  let busy = false;
  let current = hero.dataset.scene;
  let playbackRequest = 0;
  picker.hidden = false;
  motionToggle.hidden = false;

  const updateMotionLabel = () => {
    motionToggle.setAttribute('aria-label', motionEnabled ? '暂停背景动态' : '播放背景动态');
    motionToggle.querySelector('.motion-label').textContent = motionEnabled ? '暂停动态' : '播放动态';
    motionToggle.firstElementChild.textContent = motionEnabled ? 'Ⅱ' : '▷';
  };
  const shouldPlay = () => posterReady && motionEnabled && inView && !document.hidden;
  const syncMotion = () => {
    const request = ++playbackRequest;
    visuals.querySelectorAll('video').forEach((video) => {
      if (!shouldPlay() || video.closest('.hero-scene').dataset.sceneImage !== current) video.pause();
    });
    updateMotionLabel();
    if (!shouldPlay()) return;
    const frame = visuals.querySelector(`[data-scene-image="${current}"]`);
    let video = frame.querySelector('video');
    if (!video) {
      video = document.createElement('video');
      video.muted = true;
      video.defaultMuted = true;
      video.loop = true;
      video.playsInline = true;
      video.preload = 'none';
      video.setAttribute('aria-hidden', 'true');
      video.setAttribute('tabindex', '-1');
      video.poster = frame.querySelector('img').currentSrc || frame.querySelector('img').src;
      video.addEventListener('playing', () => {
        if (!shouldPlay() || frame.dataset.sceneImage !== current) { video.pause(); return; }
        frame.classList.add('video-ready');
      });
      video.addEventListener('error', () => {
        frame.classList.remove('video-ready');
        if (frame.dataset.sceneImage === current) { motionEnabled = false; updateMotionLabel(); }
      });
      frame.append(video);
    }
    const variant = narrow.matches ? 'mobile' : 'desktop';
    if (video.dataset.variant !== variant) {
      frame.classList.remove('video-ready');
      video.dataset.variant = variant;
      video.src = `${hero.dataset.videoBase}${current}-${variant}.mp4`;
    }
    if (video.error) video.load();
    // Autoplay rejection leaves the already rendered picture intact and offers manual play.
    video.play().catch((reason) => {
      if (request !== playbackRequest || reason.name === 'AbortError') return;
      if (frame.dataset.sceneImage === current && shouldPlay()) {
        motionEnabled = false;
        frame.classList.remove('video-ready');
        updateMotionLabel();
      }
    });
  };
  motionToggle.addEventListener('click', () => {
    motionEnabled = !motionEnabled;
    try { localStorage.setItem('hero-motion', motionEnabled ? 'playing' : 'paused'); } catch (_) { /* Playback still works. */ }
    syncMotion();
  });
  reducedMotion.addEventListener('change', () => {
    if (reducedMotion.matches) {
      motionEnabled = false;
      visuals.querySelectorAll('.video-ready').forEach((frame) => frame.classList.remove('video-ready'));
    }
    syncMotion();
  });
  document.addEventListener('visibilitychange', syncMotion);
  narrow.addEventListener('change', syncMotion);

  // Decode before switching. Only one transition may run, including during repeated clicks.
  const selectScene = async (button) => {
    const next = button.dataset.sceneButton;
    if (busy || next === current) return;
    busy = true;
    button.setAttribute('aria-busy', 'true');
    error.hidden = true;
    let frame = visuals.querySelector(`[data-scene-image="${next}"]`);
    let timeout;
    try {
      if (!frame) {
        const template = visuals.querySelector(`[data-scene-template="${next}"]`);
        frame = template.content.firstElementChild.cloneNode(true);
        visuals.append(frame);
      }
      const img = frame.querySelector('img');
      await Promise.race([img.decode(), new Promise((_, reject) => { timeout = setTimeout(() => reject(new Error('Image timeout')), 15000); })]);
      if (!img.naturalWidth) throw new Error('Image unavailable');
      await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
      visuals.querySelectorAll('.hero-scene').forEach((scene) => scene.classList.toggle('is-active', scene === frame));
      hero.dataset.scene = next;
      current = next;
      buttons.forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
      hero.querySelectorAll('[data-scene-caption]').forEach((caption) => { caption.hidden = caption.dataset.sceneCaption !== next; });
      syncMotion();
      if (!reducedMotion.matches) await new Promise((resolve) => setTimeout(resolve, 900));
    } catch (_) {
      if (frame && next !== current) frame.remove();
      error.hidden = false;
    } finally {
      clearTimeout(timeout);
      busy = false;
      button.removeAttribute('aria-busy');
    }
  };
  buttons.forEach((button) => button.addEventListener('click', () => selectScene(button)));
  picker.addEventListener('keydown', (event) => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    const index = buttons.indexOf(document.activeElement);
    if (index < 0) return;
    event.preventDefault();
    const next = event.key === 'Home' ? 0 : event.key === 'End' ? buttons.length - 1 : (index + (event.key === 'ArrowRight' ? 1 : -1) + buttons.length) % buttons.length;
    buttons[next].focus();
    selectScene(buttons[next]);
  });
  const header = document.querySelector('.header');
  new IntersectionObserver(([entry]) => {
    header.classList.toggle('is-scrolled', !entry.isIntersecting);
    inView = entry.isIntersecting;
    syncMotion();
  }, { rootMargin: '-80px 0px 0px 0px', threshold: 0 }).observe(hero);
  visuals.querySelector('.is-active img').decode().then(() => {
    posterReady = true;
    syncMotion();
  }).catch(() => { /* Keep the static picture path and navigation usable. */ });
  updateMotionLabel();
})();
