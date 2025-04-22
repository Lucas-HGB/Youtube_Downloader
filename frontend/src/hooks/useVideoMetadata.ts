import { useState, useEffect } from 'react';
import { extractVideoId, fetchVideoMetadata } from '../api/youtubeApi';
import { VideoMetadata } from '../types/video';

export function useVideoMetadata(url: string) {
  const [metadata, setMetadata] = useState<VideoMetadata>({
    title: '',
    author: '',
    album: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadMetadata() {
      if (!url) {
        setMetadata({ title: '', author: '', album: '' });
        setError(null);
        return;
      }

      const videoId = extractVideoId(url);
      if (!videoId) {
        setError('Invalid YouTube URL');
        return;
      }

      setIsLoading(true);
      setError(null);

      try {
        const data = await fetchVideoMetadata(videoId);
        if (data) {
          setMetadata(prev => ({
            ...prev,
            title: data.title,
            author: data.author,
          }));
          setError(null);
        } else {
          setError('Could not fetch video metadata');
        }
      } catch (err) {
        setError('Failed to load video metadata');
      } finally {
        setIsLoading(false);
      }
    }

    loadMetadata();
  }, [url]);

  return { metadata, setMetadata, isLoading, error };
}