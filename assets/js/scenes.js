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

  // Templates stay inert until requested, so later scenes do not compete with
  // the first image for bandwidth. Capture their order before adding frames.
  const scenes = [...visuals.querySelectorAll('[data-scene-image], [data-scene-template]')].map((source) => ({
    id: source.dataset.sceneImage || source.dataset.sceneTemplate,
    source,
    frame: source.matches('template') ? null : source,
  }));
  if (scenes.length < 2) return;

  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const status = hero.querySelector('.scene-status');
  const error = hero.querySelector('.scene-error');
  let currentIndex = Math.max(0, scenes.findIndex((scene) => scene.id === hero.dataset.scene));
  let busy = false;
  arrows.forEach((arrow) => { arrow.hidden = false; });

  const announceScene = () => {
    const scene = scenes[currentIndex];
    if (status) status.textContent = `背景：${scene.frame?.dataset.sceneName || scene.id}，第 ${currentIndex + 1} 张，共 ${scenes.length} 张。`;
  };
  announceScene();

  const stepScene = async (step) => {
    if (busy) return;
    const nextIndex = (currentIndex + step + scenes.length) % scenes.length;
    const next = scenes[nextIndex];
    busy = true;
    arrows.forEach((arrow) => arrow.setAttribute('aria-disabled', 'true'));
    if (status) status.setAttribute('aria-busy', 'true');
    if (error) error.hidden = true;
    let timeout;
    try {
      if (!next.frame) {
        next.frame = next.source.content.firstElementChild.cloneNode(true);
        const image = next.frame.querySelector('img');
        if (image) image.loading = 'eager';
        visuals.append(next.frame);
      }
      const image = next.frame.querySelector('img');
      if (!image) throw new Error('Image unavailable');
      await Promise.race([
        image.decode(),
        new Promise((_, reject) => { timeout = setTimeout(() => reject(new Error('Image timeout')), 15000); }),
      ]);
      if (!image.naturalWidth) throw new Error('Image unavailable');
      // Paint the decoded frame at zero opacity before starting its fade.
      await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
      visuals.querySelectorAll('.hero-scene').forEach((frame) => {
        frame.classList.toggle('is-active', frame === next.frame);
      });
      hero.dataset.scene = next.id;
      currentIndex = nextIndex;
      announceScene();
      if (!reducedMotion.matches) await new Promise((resolve) => setTimeout(resolve, 300));
    } catch (_) {
      // A failed load must never replace the picture already on screen.
      if (next.frame && nextIndex !== currentIndex && next.source.matches('template')) {
        next.frame.remove();
        next.frame = null;
      }
      if (error) error.hidden = false;
      if (status) status.textContent = error?.textContent || '背景加载暂时失败，请重试。';
    } finally {
      clearTimeout(timeout);
      busy = false;
      arrows.forEach((arrow) => arrow.removeAttribute('aria-disabled'));
      status?.removeAttribute('aria-busy');
    }
  };

  arrows.forEach((arrow) => {
    arrow.addEventListener('click', () => stepScene(Number(arrow.dataset.sceneStep)));
    arrow.addEventListener('keydown', (event) => {
      if (!['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
      event.preventDefault();
      const step = event.key === 'ArrowLeft' ? -1 : 1;
      arrows.find((item) => Number(item.dataset.sceneStep) === step)?.focus();
      stepScene(step);
    });
  });
})();
