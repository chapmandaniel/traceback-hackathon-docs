(() => {
  const searchDialog = document.querySelector('.search-dialog');
  const navDialog = document.querySelector('.mobile-nav');
  const input = document.querySelector('#doc-search');
  const results = document.querySelector('#search-results');
  const status = document.querySelector('#search-status');
  const index = window.TRACEBACK_SEARCH || [];
  const root = document.body.dataset.root || '.';
  const normal = value => value.toLocaleLowerCase();
  const openSearch = () => { if (navDialog.open) navDialog.close(); if (!searchDialog.open) searchDialog.showModal(); input.focus(); renderSearch(); };
  document.querySelectorAll('[data-search-open]').forEach(button => button.addEventListener('click', openSearch));
  document.querySelector('[data-nav-open]')?.addEventListener('click', () => {
    navDialog.showModal();
    const current = navDialog.querySelector('[aria-current="page"]');
    current?.focus();
    current?.scrollIntoView({ block: 'nearest' });
  });
  document.querySelectorAll('[data-dialog-close]').forEach(button => button.addEventListener('click', () => button.closest('dialog').close()));
  document.querySelectorAll('dialog').forEach(dialog => dialog.addEventListener('click', event => { if (event.target === dialog) { const rect = dialog.getBoundingClientRect(); if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close(); } }));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && (searchDialog.open || navDialog.open)) {
      event.preventDefault();
      (searchDialog.open ? searchDialog : navDialog).close();
      return;
    }
    const editing = ['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName) || document.activeElement?.isContentEditable;
    if ((event.key.toLowerCase() === 'k' && (event.metaKey || event.ctrlKey)) || (event.key === '/' && !editing && !searchDialog.open)) { event.preventDefault(); openSearch(); }
  });
  const highlight = (element, text, terms) => {
    if (!terms.length) { element.textContent = text; return; }
    const escaped = terms.map(term => term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
    const expression = new RegExp(`(${escaped.join('|')})`, 'gi');
    let start = 0;
    for (const match of text.matchAll(expression)) { element.append(document.createTextNode(text.slice(start, match.index))); const mark = document.createElement('mark'); mark.textContent = match[0]; element.append(mark); start = match.index + match[0].length; }
    element.append(document.createTextNode(text.slice(start)));
  };
  function renderSearch() {
    const query = input.value.trim();
    const terms = [...new Set(normal(query).split(/\s+/).filter(Boolean))];
    const ranked = index.map(page => {
      const title = normal(page.title), content = normal(page.text), group = normal(page.group);
      const matches = terms.every(term => title.includes(term) || content.includes(term) || group.includes(term));
      const score = terms.reduce((sum, term) => sum + (title.includes(term) ? 20 : 0) + (group.includes(term) ? 4 : 0) + (content.includes(term) ? 1 : 0), 0);
      return { page, matches, score };
    }).filter(result => result.matches).sort((a, b) => b.score - a.score);
    results.replaceChildren();
    const display = ranked.slice(0, terms.length ? 20 : 6);
    status.textContent = !terms.length ? 'Start typing to search all project documents.' : ranked.length ? `${ranked.length} document${ranked.length === 1 ? '' : 's'} found.` : 'No matching documents. Try a broader term, such as “evidence” or “scope”.';
    for (const { page } of display) {
      const anchor = document.createElement('a'); anchor.className = 'search-result'; anchor.href = `${root}/${page.url}`;
      const group = document.createElement('small'); group.textContent = page.group;
      const title = document.createElement('strong'); highlight(title, page.title, terms);
      const paragraph = document.createElement('p');
      const positions = terms.map(term => normal(page.text).indexOf(term)).filter(position => position >= 0);
      const position = positions.length ? Math.min(...positions) : 0;
      const start = Math.max(0, position - 65), end = Math.min(page.text.length, start + 230);
      highlight(paragraph, (start ? '…' : '') + page.text.slice(start, end) + (end < page.text.length ? '…' : ''), terms);
      anchor.append(group, title, paragraph); results.append(anchor);
    }
  }
  input.addEventListener('input', renderSearch);
  input.addEventListener('keydown', event => { if (event.key === 'ArrowDown') { event.preventDefault(); results.querySelector('a')?.focus(); } if (event.key === 'Enter') results.querySelector('a')?.click(); });
  results.addEventListener('keydown', event => {
    const links = [...results.querySelectorAll('a')]; const selected = links.indexOf(document.activeElement);
    if (event.key === 'ArrowDown') { event.preventDefault(); links[Math.min(selected + 1, links.length - 1)]?.focus(); }
    if (event.key === 'ArrowUp') { event.preventDefault(); if (selected <= 0) input.focus(); else links[selected - 1].focus(); }
  });
  const tocLinks = [...document.querySelectorAll('.page-toc .toc a')];
  const headings = tocLinks.map(link => document.getElementById(decodeURIComponent(link.hash.slice(1)))).filter(Boolean);
  let scheduled = false;
  const updateActive = () => {
    let selected = headings[0];
    for (const heading of headings) { if (heading.getBoundingClientRect().top <= 140) selected = heading; }
    tocLinks.forEach(link => { const active = link.hash === `#${selected?.id}`; link.classList.toggle('is-active', active); if (active) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current'); });
    scheduled = false;
  };
  window.addEventListener('scroll', () => { if (!scheduled) { scheduled = true; requestAnimationFrame(updateActive); } }, { passive: true });
  updateActive();
})();
