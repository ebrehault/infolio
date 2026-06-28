import type { MastodonInstance, Page } from './models';

interface State {
  path: string;
  mastodons: MastodonInstance[];
  username: string;
  pages: Page[];
  currentPage?: Page;
}

const state = $state<State>({
  path: '',
  mastodons: [],
  username: '',
  pages: [],
});

export function getState() {
  return state;
}

export function setMastodons(instances: MastodonInstance[]) {
  state.mastodons = instances;
}

export function setPages(pages: Page[]) {
  state.pages = pages;
}

export function setUsername(name: string) {
  state.username = name;
}

export function setPath(path: string) {
  state.path = path;
}
export function getPath() {
  return state.path;
}

export function setCurrentPage(currentPage: Page | undefined) {
  state.currentPage = currentPage;
}
