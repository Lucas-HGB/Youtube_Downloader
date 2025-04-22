import React from 'react';
import { VideoMetadata } from '../types/video';

interface MetadataFormProps {
  metadata: VideoMetadata;
  onChange: (metadata: VideoMetadata) => void;
  isLoading: boolean;
}

export function MetadataForm({ metadata, onChange, isLoading }: MetadataFormProps) {
  return (
    <div className="space-y-4">
      <h3 className="text-lg font-medium text-gray-900">Metadata</h3>
      
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700">
          Title
        </label>
        <input
          type="text"
          id="title"
          value={metadata.title}
          onChange={(e) => onChange({ ...metadata, title: e.target.value })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 disabled:bg-gray-100"
          required
          disabled={isLoading}
        />
      </div>

      <div>
        <label htmlFor="author" className="block text-sm font-medium text-gray-700">
          Author
        </label>
        <input
          type="text"
          id="author"
          value={metadata.author}
          onChange={(e) => onChange({ ...metadata, author: e.target.value })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 disabled:bg-gray-100"
          required
          disabled={isLoading}
        />
      </div>

      <div>
        <label htmlFor="album" className="block text-sm font-medium text-gray-700">
          Album (optional)
        </label>
        <input
          type="text"
          id="album"
          value={metadata.album}
          onChange={(e) => onChange({ ...metadata, album: e.target.value })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 disabled:bg-gray-100"
          disabled={isLoading}
        />
      </div>
    </div>
  );
}