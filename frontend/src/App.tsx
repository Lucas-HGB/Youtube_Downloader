import React, { useState, useCallback } from 'react';
import { VideoForm } from './components/VideoForm';
import { StatusDisplay } from './components/StatusDisplay';
import { VideoResponse, VideoMetadata } from './types/video';
import { submitVideo, checkVideoStatus } from './api/videoApi';
import { Music } from 'lucide-react';

export default function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState<VideoResponse | null>(null);
  const [currentMetadata, setCurrentMetadata] = useState<VideoMetadata | null>(null);
  const [selectedVideoId, setSelectedVideoId] = useState<string | null>(null);
  const [completedVideos, setCompletedVideos] = useState<Set<string>>(new Set());
  const [convertingVideos, setConvertingVideos] = useState<Set<string>>(new Set());
  const [currentlyConverting, setCurrentlyConverting] = useState<string | null>(null);

  const handleSubmit = async (url: string, metadata: VideoMetadata, videoId?: string) => {
    try {
      setIsLoading(true);
      setCurrentMetadata(metadata);
      if (videoId) {
        setSelectedVideoId(videoId);
        setConvertingVideos(prev => new Set([...prev, videoId]));
        setCurrentlyConverting(videoId);
      }
      const response = await submitVideo({ video_url: url, metadata });
      setStatus(response);

      if (response.status === 'pending' || response.status === 'processing') {
        const interval = setInterval(async () => {
          try {
            const updatedStatus = await checkVideoStatus(response.id);
            setStatus(updatedStatus);

            if (updatedStatus.status === 'completed') {
              if (videoId) {
                setCompletedVideos(prev => new Set([...prev, videoId]));
                setCurrentlyConverting(null);
              }
              clearInterval(interval);
            } else if (updatedStatus.status === 'failed') {
              setCurrentlyConverting(null);
              clearInterval(interval);
            }
          } catch (error) {
            console.error('Error checking status:', error);
            clearInterval(interval);
            setCurrentlyConverting(null);
            setStatus(prev => prev ? {
              ...prev,
              status: 'failed',
              error: 'Failed to check conversion status'
            } : null);
          }
        }, 2000);
      }
    } catch (error) {
      console.error('Submission error:', error);
      setStatus({
        id: '',
        status: 'failed',
        error: error instanceof Error ? error.message : 'Failed to process video',
      });
      setCurrentlyConverting(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-4xl mx-auto py-12 px-4">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <Music className="w-12 h-12 text-indigo-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900">
            YouTube to MP3 Converter
          </h1>
          <p className="mt-2 text-gray-600">
            Download YouTube videos as MP3s with custom metadata
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <VideoForm 
            onSubmit={handleSubmit} 
            isLoading={isLoading} 
            completedVideos={completedVideos}
            convertingVideos={convertingVideos}
            currentlyConverting={currentlyConverting}
            selectedVideoId={selectedVideoId}
            onVideoSelect={setSelectedVideoId}
          />
          {status && (
            <StatusDisplay 
              status={status} 
              metadata={currentMetadata} 
              selectedVideoId={selectedVideoId}
              completedVideos={completedVideos}
              convertingVideos={convertingVideos}
              currentlyConverting={currentlyConverting}
            />
          )}
        </div>
      </div>
    </div>
  );
}