import { useState, useCallback } from 'react';
import { PlaylistVideo } from '../types/video';

export function usePlaylistConversion() {
  const [convertingVideos] = useState(new Set<string>());
  const [notifications, setNotifications] = useState<Array<{ id: string; message: string }>>([]);

  const addNotification = useCallback((message: string) => {
    const id = Date.now().toString();
    setNotifications(prev => [...prev, { id, message }]);
    setTimeout(() => {
      setNotifications(prev => prev.filter(n => n.id !== id));
    }, 5000);
  }, []);

  return {
    convertingVideos,
    notifications,
    setNotifications,
    addNotification,
  };
}