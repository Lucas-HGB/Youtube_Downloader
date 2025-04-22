import { useState, useEffect } from 'react';
import { extractPlaylistId, fetchPlaylistMetadata } from '../api/youtubeApi';
import { fetchPlaylistMetadata } from '../api/videoApi';
import { PlaylistMetadata, VideoMetadata } from '../types/video';

export function usePlaylist(url: string) {
  const [playlistData, setPlaylistData] = useState<PlaylistMetadata | null>(null);
  const [currentVideo, setCurrentVideo] = useState<VideoMetadata>({
    title: '',
    author: '',
    album: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadPlaylist() {
      if (!url) {
        setPlaylistData(null);
        setError(null);
        return;
      }

      const playlistId = extractPlaylistId(url);
      if (!playlistId) {
        setError('Invalid YouTube playlist URL');
        return;
      }

      setIsLoading(true);
      setError(null);

      try {
        const data = await fetchPlaylistMetadata(playlistId);
        if (data) {
          setPlaylistData(data);
          // Initialize with first video's metadata
          if (data.videos.length > 0) {
            setCurrentVideo({
              title: data.videos[0].title,
              author: data.videos[0].author,
              album: data.title,
            });
          }
        } else {
          setError('Could not fetch playlist data');
        }
      } catch (err) {
        setError('Failed to load playlist');
      } finally {
        setIsLoading(false);
      }
    }

    loadPlaylist();
  }, [url]);

  return {
    playlistData,
    currentVideo,
    setCurrentVideo,
    isLoading,
    error,
  };
}