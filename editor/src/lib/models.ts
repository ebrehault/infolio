export interface MastodonInstance {
  id: string;
}

export type APIResponse<T> = APISuccess<T> | APIError;

export interface APISuccess<T> {
  success: true;
  response: T;
}

export interface APIError {
  success: false;
  code: number;
  message: string;
}

export interface Page {
  id: string;
  title: string;
  created: string;
  modified: string;
  code?: string;
}
