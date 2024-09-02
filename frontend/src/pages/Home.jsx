import React, { useContext, useEffect, useState } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import Header from '../components/navbar/Navbar';
import Footer from '../components/footer/Footer';
import { useTheme } from '../contexts/ThemeContext';
import '../App.css';
import '../Theme.css';
import AuthContext from '../contexts/AuthContext';
import { jwtDecode } from 'jwt-decode';

const Home = () => {
  const { isAuth, token, setIsAuth } = useContext(AuthContext);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const { iat, exp } = jwtDecode(token);
  const TIME_OUT = exp - iat;

  useEffect(() => {
    if (!isAuth) {
      navigate('/login');
    } else {
      const interval = setInterval(() => {
        setIsAuth(false);
        navigate('/login');
      }, TIME_OUT * 1000);
      return () => clearInterval(interval);
    }
  }, [isAuth, navigate, setIsAuth, TIME_OUT]);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <div className={`app app-${theme} ${sidebarOpen ? 'sidebar-open' : ''}`} style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Sidebar />
      <div className="main-content" style={{ display: 'flex', flexDirection: 'column', flexGrow: 1 }}>
        <Header
          toggleSidebar={toggleSidebar}
          toggleTheme={toggleTheme}
          theme={theme}
        />
        <main style={{ flexGrow: 1 }}>
          <Outlet /> {/* This is where nested routes will render */}
        </main>
      </div>
      <Footer />
    </div>
  );
};

export default Home;