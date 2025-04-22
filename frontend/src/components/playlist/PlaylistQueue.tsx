import React from 'react';
import { PlaylistVideo } from '../../types/video';
import { PlaylistItem } from './PlaylistItem';

interface PlaylistQueueProps {
  videos: PlaylistVideo[];
  convertingVideos: Set<string>;
  completedVideos: Set<string>;
  currentlyConverting: string | null;
  onVideoSelect: (video: PlaylistVideo) => void;
  selectedVideoId: string | null;
}

export function PlaylistQueue({
  videos,
  convertingVideos,
  completedVideos,
  currentlyConverting,
  onVideoSelect,
  selectedVideoId,
}: PlaylistQueueProps) {
  return (
    <div className="space-y-2 max-h-96 overflow-y-auto">
      {videos.map((video) => (
        <PlaylistItem
          key={video.id}
          video={video}
          isConverting={convertingVideos.has(video.id)}
          isCompleted={completedVideos.has(video.id)}
          isSelected={video.id === selectedVideoId}
          isCurrentlyConverting={video.id === currentlyConverting}
          onClick={() => onVideoSelect(video)}
        />
      ))}
    </div>
  );
}