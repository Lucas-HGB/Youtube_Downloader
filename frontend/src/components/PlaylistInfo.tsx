import React from 'react';
import { PlaylistMetadata } from '../types/video';
import { ListMusic } from 'lucide-react';

interface PlaylistInfoProps {
  playlist: PlaylistMetadata;
}

export function PlaylistInfo({ playlist }: PlaylistInfoProps) {
  return (
    <div className="mb-6 bg-gray-50 rounded-lg p-4">
      <div className="flex items-center gap-2 mb-3">
        <ListMusic className="w-5 h-5 text-indigo-600" />
        <h2 className="text-lg font-semibold text-gray-900">{playlist.title}</h2>
      </div>
      
      <div className="text-sm text-gray-600">
        <p>Processing video {playlist.currentIndex + 1} of {playlist.videos.length}</p>
      </div>

      <div className="mt-3 max-h-32 overflow-y-auto">
        <ul className="space-y-2">
          {playlist.videos.map((video, index) => (
            <li
              key={video.id}
              className={`text-sm p-2 rounded ${
                index === playlist.currentIndex
                  ? 'bg-indigo-50 text-indigo-700'
                  : index < playlist.currentIndex
                  ? 'text-gray-400'
                  : 'text-gray-700'
              }`}
            >
              {video.title}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}