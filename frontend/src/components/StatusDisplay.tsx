import React from 'react';
import { VideoResponse } from '../types/video';
import { Download, AlertCircle, Clock, Loader2 } from 'lucide-react';
import { getDownloadUrl } from '../utils/download';

interface StatusDisplayProps {
  status: VideoResponse;
  metadata?: { title: string };
  selectedVideoId?: string | null;
  completedVideos: Set<string>;
  convertingVideos: Set<string>;
}

export function StatusDisplay({ 
  status, 
  metadata, 
  selectedVideoId, 
  completedVideos,
  convertingVideos
}: StatusDisplayProps) {
  // Only show status for videos that have started conversion
  if (!selectedVideoId || !convertingVideos.has(selectedVideoId)) {
    return null;
  }

  const isSelectedVideoCompleted = selectedVideoId && completedVideos.has(selectedVideoId);

  const getStatusDisplay = () => {
    switch (status.status) {
      case 'pending':
        return (
          <div className="flex items-center gap-2 text-yellow-600">
            <Clock className="w-5 h-5 animate-pulse" />
            <span>Waiting to process...</span>
          </div>
        );
      case 'processing':
        return (
          <div className="flex items-center gap-2 text-blue-600">
            <Loader2 className="w-5 h-5 animate-spin" />
            <span>Converting video to MP3...</span>
          </div>
        );
      case 'completed':
        if (isSelectedVideoCompleted) {
          const downloadUrl = getDownloadUrl(metadata?.title || 'download');
          return (
            <div className="flex flex-col items-center gap-4">
              <div className="text-green-600">Conversion completed!</div>
              <a
                href={downloadUrl}
                className="flex items-center gap-2 py-2 px-4 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
                download={`${metadata?.title || 'download'}.mp3`}
              >
                <Download className="w-4 h-4" />
                Download MP3
              </a>
            </div>
          );
        }
        return null;
      case 'failed':
        return (
          <div className="flex items-center gap-2 text-red-600">
            <AlertCircle className="w-5 h-5" />
            <span>Error: {status.error}</span>
          </div>
        );
    }
  };

  return (
    <div className="mt-6 p-4 bg-white rounded-lg shadow">
      {getStatusDisplay()}
    </div>
  );
}