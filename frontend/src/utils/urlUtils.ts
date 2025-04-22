// Extract video or playlist IDs from YouTube URLs
export function extractYouTubeIds(url: string) {
  // Clean and normalize the URL
  const cleanUrl = url.trim();
  
  // Extract video ID
  const videoIdMatch = cleanUrl.match(/[?&]v=([^&]+)/);
  const videoId = videoIdMatch ? videoIdMatch[1] : null;
  
  // Extract playlist ID
  const playlistIdMatch = cleanUrl.match(/[?&]list=([^&]+)/);
  const playlistId = playlistIdMatch ? playlistIdMatch[1] : null;
  
  return { videoId, playlistId };
}