import { useState } from "react";
import '../style/Header.css'
import SearchIcon from "@mui/icons-material/Search";
import NotificationsIcons from "@mui/icons-material/Notifications";
import SettingsIcon from '@mui/icons-material/Settings';
import { Link } from "react-router-dom";

function Header() {
  const [inputSearch, setInputSearch] = useState('');
  return (
    <div className='header'>
        <div className='header_left' >
            <img className='header_logo' src='https://upload.wikimedia.org/wikipedia/commons/5/54/YouTube_dark_logo_2017.svg' alt=''/>
        </div>
        <div className='header_input'>
            <input onChange={e => setInputSearch(e.target.value)} value={inputSearch} type="text" placeholder='Search' id='header_searchInput'/>
            <Link to={`/search/${inputSearch}`}>
              <SearchIcon className='header_inputButton'/>
            </Link>
                
        </div>
        
        <div className='header_right'>
            <NotificationsIcons className='header_icon'/>
            <SettingsIcon className='header_icon'/>
        </div>
    </div>
  )
}

export default Header