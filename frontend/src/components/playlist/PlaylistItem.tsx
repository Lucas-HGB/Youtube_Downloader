import React from 'react';
import { PlaylistVideo } from '../../types/video';
import { Check, Loader2 } from 'lucide-react';

interface PlaylistItemProps {
  video: PlaylistVideo;
  isConverting: boolean;
  isCompleted: boolean;
  isSelected: boolean;
  isCurrentlyConverting: boolean;
  onClick: () => void;
}

export function PlaylistItem({ 
  video, 
  isConverting, 
  isCompleted, 
  isSelected, 
  isCurrentlyConverting,
  onClick 
}: PlaylistItemProps) {
  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-3 rounded-md flex items-center gap-3 hover:bg-gray-50 transition-colors
        ${isConverting ? 'bg-blue-50' : ''}
        ${isCompleted ? 'bg-green-50' : ''}
        ${isSelected ? 'ring-2 ring-indigo-500' : ''}`}
    >
      <img
        src={video.thumbnail}
        alt={video.title}
        className="w-16 h-12 object-cover rounded"
      />
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-900 truncate">{video.title}</p>
        <p className="text-sm text-gray-500 truncate">{video.author}</p>
      </div>
      {isCurrentlyConverting && <Loader2 className="w-4 h-4 text-blue-600 animate-spin" />}
      {isCompleted && !isCurrentlyConverting && <Check className="w-4 h-4 text-green-600" />}
    </button>
  );
}