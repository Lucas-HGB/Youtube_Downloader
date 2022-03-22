import VideoDescription from "../components/VideoDescription";
import VideoPlayer from "../components/VideoPlayer";
import "../style/VideoPage.css";
import { useParams } from 'react-router';

const VideoPage = ({ ytbUrl }) => {
  // let videoID = JSON.stringify(useParams());
  // console.log(videoID);
  return (
    <div className="video_page">
        {/* <code>{JSON.stringify(match, null, 2)}</code>
        <code>{JSON.stringify(location, null, 2)}</code> */}
        <VideoPlayer/>
        <VideoDescription/>
    </div>
  )
}

export default VideoPage