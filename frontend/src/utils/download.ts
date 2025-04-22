export function getDownloadUrl(title: string): string {
  // Get the current origin (protocol + hostname + port)
  const origin = window.location.origin;
  
  // Sanitize the filename by removing invalid characters
  const sanitizedTitle = title.replace(/[<>:"/\\|?*]/g, '_');
  
  // Construct the download URL using the current origin
  return `${origin}/app/downloads/${encodeURIComponent(sanitizedTitle)}.mp3`;
}