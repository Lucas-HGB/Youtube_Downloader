import { PlaylistMetadata, PlaylistVideo } from '../types/video';
import { extractYouTubeIds } from '../utils/urlUtils';

// Extract video ID from YouTube URL
export function extractVideoId(url: string): string | null {
  return extractYouTubeIds(url).videoId;
}

export function extractPlaylistId(url: string): string | null {
  return extractYouTubeIds(url).playlistId;
}

export async function fetchVideoMetadata(videoId: string) {
  try {
    const response = await fetch(
      `https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=${videoId}&format=json`
    );

    if (!response.ok) {
      throw new Error('Failed to fetch video metadata');
    }

    const data = await response.json();
    return {
      title: data.title,
      author: data.author_name,
      thumbnail: `https://img.youtube.com/vi/${videoId}/mqdefault.jpg`,
    };
  } catch (error) {
    console.error('Error fetching video metadata:', error);
    return null;
  }
}