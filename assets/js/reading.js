(() => {
  document.querySelectorAll(".post-content .highlight").forEach((block) => {
    const code = block.querySelector("code[data-lang]");
    if (code) block.dataset.language = code.dataset.lang;
  });

  document.querySelectorAll("[data-reader-panel]").forEach((panel) => {
    const narrow = window.matchMedia(`(max-width: ${panel.dataset.readerPanel}px)`);
    const updatePanel = () => { panel.open = !narrow.matches; };
    updatePanel();
    narrow.addEventListener("change", updatePanel);
  });

  const toc = document.querySelector(".note-toc-content");
  if (!toc) return;

  // Keep long technical outlines navigable without hiding their structure.
  toc.querySelectorAll("li").forEach((item) => {
    const children = Array.from(item.children);
    const childList = children.find((child) => child.tagName === "UL");
    const link = children.find((child) => child.tagName === "A");
    if (!childList || !link) return;
    const button = document.createElement("button");
    button.type = "button";
    button.className = "note-toc-node-toggle";
    button.setAttribute("aria-label", `折叠 ${link.textContent} 的子标题`);
    button.setAttribute("aria-expanded", "true");
    button.innerHTML = '<span aria-hidden="true">⌄</span>';
    link.before(button);
    item.classList.add("has-children");
    button.addEventListener("click", () => {
      childList.hidden = !childList.hidden;
      button.setAttribute("aria-expanded", String(!childList.hidden));
      button.setAttribute("aria-label", `${childList.hidden ? "展开" : "折叠"} ${link.textContent} 的子标题`);
    });
  });

  const links = Array.from(toc.querySelectorAll('a[href^="#"]'));
  const headings = links.map((link) => ({
    link,
    heading: document.getElementById(decodeURIComponent(link.hash.slice(1))),
  })).filter((entry) => entry.heading);
  if (!headings.length) return;

  let active = null;
  let scheduled = false;
  const updateCurrent = () => {
    scheduled = false;
    const headerHeight = parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--header-height")) || 68;
    let current = headings[0];
    for (const entry of headings) {
      if (entry.heading.getBoundingClientRect().top > headerHeight + 32) break;
      current = entry;
    }
    if (current === active) return;
    active?.link.removeAttribute("aria-current");
    current.link.setAttribute("aria-current", "location");
    active = current;
  };
  const scheduleUpdate = () => {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(updateCurrent);
  };
  window.addEventListener("scroll", scheduleUpdate, { passive: true });
  window.addEventListener("resize", scheduleUpdate);
  updateCurrent();
})();
