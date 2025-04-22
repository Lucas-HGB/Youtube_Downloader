export const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://api.ytdl.hoeltgebaum.net';

export const API_ENDPOINTS = {
  SUBMIT_VIDEO: `${API_BASE_URL}/videos`,
  CHECK_STATUS: (id: string) => `${API_BASE_URL}/videos/${id}`,
  FETCH_PLAYLIST_METADATA: `${API_BASE_URL}/youtube-api/playlist/metadata`,
} as const;
