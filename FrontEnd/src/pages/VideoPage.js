import VideoDescription from "../components/VideoDescription";
import VideoPlayer from "../components/VideoPlayer";
import "../style/VideoPage.css";
import { update_video } from "../functions/API";
import { useParams } from 'react-router';


function VideoPage () {
  let {searchUrl} = useParams();
  update_video(searchUrl);
  return (
    <div className="video_page">
        <VideoPlayer searchUrl={searchUrl}/>
        <VideoDescription/>
    </div>
  )
}

export default VideoPage