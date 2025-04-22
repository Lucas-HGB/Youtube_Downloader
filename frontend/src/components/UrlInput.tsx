import React from 'react';
import { AlertCircle } from 'lucide-react';

interface UrlInputProps {
  url: string;
  onChange: (url: string) => void;
  error: string | null;
  isLoading: boolean;
}

export function UrlInput({ url, onChange, error, isLoading }: UrlInputProps) {
  return (
    <div>
      <label htmlFor="url" className="block text-sm font-medium text-gray-700">
        YouTube URL
      </label>
      <div className="mt-1">
        <input
          type="url"
          id="url"
          value={url}
          onChange={(e) => onChange(e.target.value)}
          className={`block w-full rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 ${
            error ? 'border-red-300' : 'border-gray-300'
          } disabled:bg-gray-100`}
          placeholder="https://youtube.com/watch?v=..."
          required
          disabled={isLoading}
        />
      </div>
      {error && (
        <div className="mt-2 text-sm text-red-600 flex items-center gap-1">
          <AlertCircle className="w-4 h-4" />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
}