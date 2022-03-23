import './style/App.css';
import Header from './components/Header';
import VideoPage from "./pages/VideoPage";
import ConfigsPage from "./pages/ConfigsPage";

import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";


function App() {
  return (
    <div className="app">
      <Router>
        <Header/>
        <div className='app_page'>
          <Routes>
            <Route exact path="/search/:searchUrl" element={<VideoPage />}/>
            <Route exact path="/configs" element={<ConfigsPage />}/>
          </Routes>
        </div>
      </Router>
    </div>
  );
}

export default App;
