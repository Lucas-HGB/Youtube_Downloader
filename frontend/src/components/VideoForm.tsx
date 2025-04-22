import React, { useState, useCallback } from 'react';
import { VideoMetadata, PlaylistVideo } from '../types/video';
import { Music } from 'lucide-react';
import { useVideoMetadata } from '../hooks/useVideoMetadata';
import { usePlaylist } from '../hooks/usePlaylist';
import { usePlaylistConversion } from '../hooks/usePlaylistConversion';
import { UrlInput } from './UrlInput';
import { MetadataForm } from './MetadataForm';
import { PlaylistQueue } from './playlist/PlaylistQueue';
import { NotificationList } from './notifications/NotificationList';
import { extractPlaylistId } from '../api/youtubeApi';

interface VideoFormProps {
  onSubmit: (url: string, metadata: VideoMetadata, videoId?: string) => Promise<void>;
  isLoading: boolean;
  completedVideos: Set<string>;
  convertingVideos: Set<string>;
  currentlyConverting: string | null;
  selectedVideoId: string | null;
  onVideoSelect: (videoId: string | null) => void;
}

export function VideoForm({ 
  onSubmit, 
  isLoading, 
  completedVideos, 
  convertingVideos,
  currentlyConverting,
  selectedVideoId,
  onVideoSelect 
}: VideoFormProps) {
  const [url, setUrl] = useState('');
  const [selectedVideo, setSelectedVideo] = useState<PlaylistVideo | null>(null);
  const isPlaylist = !!extractPlaylistId(url);
  
  const {
    metadata: singleVideoMetadata,
    setMetadata: setSingleVideoMetadata,
    isLoading: isLoadingVideo,
    error: videoError
  } = useVideoMetadata(isPlaylist ? '' : url);

  const {
    playlistData,
    currentVideo,
    setCurrentVideo,
    isLoading: isLoadingPlaylist,
    error: playlistError,
  } = usePlaylist(isPlaylist ? url : '');

  const {
    notifications,
    setNotifications,
    addNotification
  } = usePlaylistConversion();

  const metadata = isPlaylist ? currentVideo : singleVideoMetadata;
  const setMetadata = isPlaylist ? setCurrentVideo : setSingleVideoMetadata;
  const error = isPlaylist ? playlistError : videoError;
  const isLoadingMetadata = isPlaylist ? isLoadingPlaylist : isLoadingVideo;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      if (isPlaylist && selectedVideo) {
        const videoUrl = `https://youtube.com/watch?v=${selectedVideo.id}`;
        await onSubmit(videoUrl, metadata, selectedVideo.id);
      } else {
        await onSubmit(url, metadata);
      }
    } catch (error) {
      console.error('Conversion failed:', error);
    }
  };

  const handleVideoSelect = useCallback((video: PlaylistVideo) => {
    setSelectedVideo(video);
    onVideoSelect(video.id);
    setCurrentVideo({
      title: video.title,
      author: video.author,
      album: playlistData?.title || '',
    });
  }, [playlistData, setCurrentVideo, onVideoSelect]);

  // Show notification when a video completes conversion
  React.useEffect(() => {
    const lastCompletedVideo = Array.from(completedVideos).pop();
    if (lastCompletedVideo && playlistData) {
      const video = playlistData.videos.find(v => v.id === lastCompletedVideo);
      if (video) {
        addNotification(`✅ ${video.title} has been converted successfully!`);
      }
    }
  }, [completedVideos, playlistData, addNotification]);

  return (
    <div className="space-y-6">
      <UrlInput
        url={url}
        onChange={setUrl}
        error={error}
        isLoading={isLoading}
      />

      {playlistData && (
        <PlaylistQueue
          videos={playlistData.videos}
          convertingVideos={convertingVideos}
          completedVideos={completedVideos}
          currentlyConverting={currentlyConverting}
          onVideoSelect={handleVideoSelect}
          selectedVideoId={selectedVideoId}
        />
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <MetadataForm
          metadata={metadata}
          onChange={setMetadata}
          isLoading={isLoading || isLoadingMetadata}
        />

        <button
          type="submit"
          disabled={isLoading || isLoadingMetadata || !!error || (isPlaylist && !selectedVideo)}
          className="w-full flex justify-center items-center gap-2 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Music className="w-4 h-4" />
          {isLoading ? 'Processing...' : 'Convert to MP3'}
        </button>
      </form>

      <NotificationList
        notifications={notifications}
        onDismiss={(id) => {
          setNotifications(prev => prev.filter(n => n.id !== id));
        }}
      />
    </div>
  );
}