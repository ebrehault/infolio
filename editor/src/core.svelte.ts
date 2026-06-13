import { API } from './lib/api';
import { getState, setMastodons, setPages, setUsername } from './lib/store.svelte';

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
  API.createAccount().then((res) => console.log(res));
}
export function addPage() {
  API.addPage(getState().username, 'test', 'Test', 'Hello').then((res) => loadPages());
}
export function deletePage(id: string) {
  API.deletePage(`${getState().username}/${id}`).then((res) => loadPages());
}
