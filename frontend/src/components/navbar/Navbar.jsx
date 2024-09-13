import React, { useContext } from 'react';
import './Navbar.css';
import { useTheme } from '../../contexts/ThemeContext';
import AuthContext from '../../contexts/AuthContext';

// Import Material-UI icons
import LightModeIcon from '@mui/icons-material/LightMode';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import IconButton from '@mui/material/IconButton';
import LogoutIcon from '@mui/icons-material/Logout';


const Navbar = ({ toggleSidebar }) => {
  const { theme, toggleTheme } = useTheme();
  const { logout } = useContext(AuthContext);

  return (
    <header className={`header header-${theme}`}>
      <button className='menu-toggle' onClick={toggleSidebar}>
        ☰
      </button>
      <h1 className={`header-txt header-text-${theme}`}>Dashboard</h1>
      <div className='user-info'>
        <span className={`header-text-${theme}`}>Welcome, Admin</span>
        <IconButton color="inherit">
          <AccountCircleIcon fontSize="large" />
        </IconButton>
        <IconButton onClick={toggleTheme} color="inherit">
          {theme === 'light' ? <DarkModeIcon /> : <LightModeIcon />}
        </IconButton>
        <IconButton onClick={logout} color="inherit">
  <LogoutIcon />
</IconButton>

      </div>
    </header>
  );
};

export default Navbar;
