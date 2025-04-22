export interface VideoMetadata {
  title: string;
  author: string;
  album?: string;
}

export interface VideoRequest {
  video_url: string;
  metadata: VideoMetadata;
}

export interface VideoResponse {
  id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  downloadUrl?: string;
  error?: string;
}

export interface PlaylistVideo {
  id: string;
  title: string;
  author: string;
  thumbnail: string;
}

export interface PlaylistMetadata {
  videos: PlaylistVideo[];
  currentIndex: number;
  title: string;
}