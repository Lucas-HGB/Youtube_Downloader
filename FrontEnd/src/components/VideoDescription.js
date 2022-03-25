import React from 'react';
import "../style/VideoDescription.css";
import { get_metadata } from "../functions/API";

function VideoDescription({ searchUrl }) {
  var metadata = get_metadata(searchUrl);
  console.log(metadata);
  return (
    <div className='video_description'>
        VideoDescription
    </div>
  )
}

export default VideoDescription