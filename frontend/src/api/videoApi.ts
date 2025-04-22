import { VideoRequest, VideoResponse } from '../types/video';
import { API_ENDPOINTS } from './config';

export async function submitVideo(request: VideoRequest): Promise<VideoResponse> {
  const response = await fetch(API_ENDPOINTS.SUBMIT_VIDEO, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to submit video' }));
    throw new Error(error.detail || 'Failed to submit video');
  }

  return response.json();
}

export async function checkVideoStatus(id: string): Promise<VideoResponse> {
  const response = await fetch(API_ENDPOINTS.CHECK_STATUS(id));

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to check video status' }));
    throw new Error(error.detail || 'Failed to check video status');
  }

  return response.json();
}

export async function fetchPlaylistMetadata(playlistId: string): Promise<PlaylistMetadata | null> {
  try {
      const payload = {
        part: 'snippet',
        max_results: 200,
        playlist_id: playlistId
      };
      const response = await fetch(API_ENDPOINTS.FETCH_PLAYLIST_METADATA, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
          throw new Error('Server responded with an error');
      }

      const data = await response.json();
      console.log(data);

      // If there are no items, return null to indicate no data
      if (data.items && data.items.length === 0) {
          return null;
      }

      const videos = data.items.map((item: any) => ({
          id: item.snippet.resourceId.videoId,
          title: item.snippet.title,
          author: item.snippet.videoOwnerChannelTitle,
          thumbnail: item.snippet.thumbnails.medium.url,
      }));

      return {
          title: data.items[0]?.snippet.title || 'YouTube Playlist',
          videos,
          currentIndex: 0,
      };
  } catch (error) {
      console.error('Error fetching playlist metadata:', error);
      return null;
  }
}