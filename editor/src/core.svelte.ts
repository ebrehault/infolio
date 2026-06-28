import { API } from './lib/api';
import { getState, setCurrentPage, setMastodons, setPages, setUsername } from './lib/store.svelte';

export function initLogin() {
  const url = new URL(location.href);
  const token = url.searchParams.get('token');
  if (token) {
    API.setAuthToken(token);
  }
  if (API.isLoggedIn()) {
    API.getProfile().then((res) => {
      console.log(res);
      if (res.success) {
        setUsername(res.response);
      } else {
        console.error(res.message);
      }
    });
  } else {
    const instance = API.getInstance();
    if (instance) {
      setMastodons([{ id: instance }]);
    } else {
      API.loadMastodonInstances().then((instances) => setMastodons(instances));
    }
  }
}

export function loadPages() {
  if (getState().username) {
    const path = getState().username;
    API.getPages(path).then((res) => {
      if (res.success) {
        setPages(res.response);
      } else {
        setPages([]);
      }
    });
  }
}

export function createAccount() {
  return API.createAccount().then((res) => console.log(res));
}
export function getPage(path: string) {
  return API.getPage(`${getState().username}/${path}`).then((res) => {
    if (res.success) {
      setCurrentPage(res.response);
    } else {
      setCurrentPage(undefined);
    }
  });
}
export function addPage() {
  return API.addPage(getState().username, 'test', 'Test', 'Hello').then((res) => loadPages());
}
export function deletePage(path: string) {
  return API.deletePage(`${getState().username}/${path}`).then((res) => loadPages());
}
export function editPage(path: string, data: { title?: string; body?: string }) {
  return API.modifyPage(`${getState().username}/${path}`, data).then((res) => loadPages());
}
export function publishPage(path: string) {
  return API.publishPage(`${getState().username}/${path}`);
}
