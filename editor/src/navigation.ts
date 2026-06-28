import { setPath } from './lib/store.svelte';

export function initNavigation() {
  // Adapted from https://github.com/sveltejs/kit/blob/master/packages/kit/src/runtime/client/router.js
  if ('scrollRestoration' in history) {
    history.scrollRestoration = 'manual';
  }
  addEventListener('beforeunload', () => {
    history.scrollRestoration = 'auto';
  });
  addEventListener('load', () => {
    history.scrollRestoration = 'manual';
  });
  addEventListener('click', (event) => {
    if (event.button || event.which !== 1) return;
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    if (event.defaultPrevented) return;

    const a = find_anchor(event.target);
    if (!a) return;
    if (!a.href) return;
    const rel = (a.getAttribute('rel') || '').split(/\s+/);
    if (a.hasAttribute('download') || (rel && rel.includes('external'))) {
      return;
    }
    if (a instanceof SVGAElement ? a.target.baseVal : a.target) return;

    const svg = typeof a.href === 'object' && a.href.constructor.name === 'SVGAnimatedString';
    const href = String(svg ? a.href.baseVal : a.href);

    if (href === location.href) {
      if (!location.hash) event.preventDefault();
      return;
    }
    event.preventDefault();
    navigate(href);
  });
  onpopstate = (event) => {
    navigate(document.location.pathname);
  };
  navigate(location.href);
}
function find_anchor(node: any) {
  while (node && node.nodeName.toUpperCase() !== 'A') node = node.parentNode;
  return node;
}

export function navigate(url: string) {
  console.log('nav to', url);
  history.pushState({}, '', url);
  const path = new URL(url).pathname;
  setPath(path.slice(1));
}
