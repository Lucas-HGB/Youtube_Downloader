import React from 'react';
import "../style/VideoPlayer.css";

function VideoPlayer({ searchUrl }) {
  return (
    <div className='video_player-container'>
      <iframe
        className='player_frame'
        src={`https://www.youtube.com/embed/${searchUrl}?rel=0&modestbranding=1`}
        frameBorder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
        title="Embedded youtube"
      />
    </div>
  )
}

export default VideoPlayer