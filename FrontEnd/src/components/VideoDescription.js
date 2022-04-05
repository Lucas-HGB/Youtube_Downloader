import React, {useState, useEffect} from 'react';
import "../style/VideoDescription.css";
import { get_metadata } from "../functions/API";

function VideoDescription({ searchUrl }) {
  // var metadata = get_metadata(searchUrl);
  let [metadata, set_metadata] = useState({});


  useEffect(async function() {set_metadata(await get_metadata(searchUrl));} , []);
  return (
    <div className='video_description'>
        {metadata["title"]}
    </div>
  )
}

export default VideoDescription