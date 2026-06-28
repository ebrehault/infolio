import type { APIError, APIResponse, MastodonInstance, Page } from './models';

const BACKEND = 'http://localhost:8080/db/container';
// const BACKEND = 'https://109b-82-64-57-232.ngrok-free.app/db/container';
const TOKEN_KEY = 'token';
const INSTANCE_KEY = 'instance';
export const API = {
  setAuthToken: (token: string) => {
    localStorage.setItem(TOKEN_KEY, token);
  },
  setInstance: (instance: string) => {
    localStorage.setItem(INSTANCE_KEY, instance);
  },
  getInstance: () => {
    return localStorage.getItem(INSTANCE_KEY);
  },
  isLoggedIn: () => {
    return !!localStorage.getItem(TOKEN_KEY);
  },
  logout: () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(INSTANCE_KEY);
  },

  loadMastodonInstances: (): Promise<MastodonInstance[]> => {
    return fetch(`${BACKEND}/mastodons/@list`).then((res) => res.json());
  },

  getLoginUrl: (instance: string) => {
    return `${BACKEND}/mastodons/${instance}/@login`;
  },

  getProfile: (): Promise<APIResponse<string>> => {
    return fetchAPI<string>('@profile');
  },

  getAccount: () => {
    return fetchAPI('@get_account_data');
  },

  createAccount: () => {
    return fetchAPI('@create_account', 'POST', {});
  },

  getPages: (path: string) => {
    return fetchAPI<Page[]>(`@get_pages`);
  },

  getPage: (path: string) => {
    return fetchAPI<Page>(path);
  },

  addPage: (path: string, id: string, title: string, body?: string) => {
    return fetchAPI<any>(path, 'POST', { '@type': 'Page', id, title, body });
  },

  modifyPage: (path: string, data: { title?: string; body?: string }) => {
    return fetchAPI<any>(path, 'PATCH', data);
  },

  deletePage: (path: string) => {
    return fetchAPI(path, 'DELETE');
  },

  publishPage: (path: string) => {
    return fetchAPI(`${path}/@publish`, 'POST');
  },
};
function fetchAPI<T>(path: string, method = 'GET', body?: any): Promise<APIResponse<T>> {
  const token = localStorage.getItem(TOKEN_KEY);
  const instance = localStorage.getItem(INSTANCE_KEY);
  if (!token || !instance) {
    throw 'Not authenticated';
  }
  const params: any = {
    method,
    headers: {
      Authorization: 'Bearer ' + token,
      'content-type': 'application/json',
    },
  };
  if (body) {
    params.body = JSON.stringify(body);
  }
  return fetch(`${BACKEND}/mastodons/${instance}/${path}`, params).then((res) => {
    if (!res.ok) {
      return { error: true, code: res.status, message: res.statusText };
    }
    return res.json().then((response) => ({ success: true, response }));
  });
}
