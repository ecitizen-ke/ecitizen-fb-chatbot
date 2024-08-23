import React, { createContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import useLocalStorage from '../hooks/useLocalStorage';
import { Config } from '../Config';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const navigate = useNavigate();
  const [isAuth, setIsAuth] = useState(false);
  const [token, setToken] = useLocalStorage('token');

  const login = async ({email,password}) => {
    // e.preventDefault();
    try {
      const res = await fetch(
        `${Config.API_URL}/auth/login`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email,
            password,
          }),
        }
      );
      if (res.status === 200) {
        const response = await res.json();
        setToken(response.access_token);
        localStorage.setItem('refresh_token', response.refresh_token);
        setIsAuth(true);
        navigate('/');
      }
    } catch (error) {
      console.log(error);
    }
  };

  const logout = async () => {


    try {
      const res = await fetch(
        `${Config.API_URL}/auth/logout`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + token,
          },
        }
      );

      if (res.status === 200) {
        setIsAuth(false);
        localStorage.removeItem('token')
        localStorage.removeItem('refresh_token')
        navigate('/login');
      } else {
        const result = await res.json();
        console.log(result);

        if(res.status === 401){
          localStorage.removeItem('token');
          // window.location.reload();
          navigate('/login')
        }
    
      }
    } catch (error) {
      console.log(error);
     
    }
  };

  const getNewAccessToken = async () => {
    try {
      const res = await fetch(
        `${Config.API_URL}/auth/refresh`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer '+localStorage.getItem('refresh_token'),
          },
        }
      );

      if (res.status === 200) {
        const response = await res.json();
        setToken(response.access_token);
        // window.location.reload();
        localStorage.setItem('refresh_token', response.access_token);
        console.log('New token generated ',response.access_token)
      } else {
        console.log('User logged out');
        
        localStorage.removeItem('token');
        localStorage.removeItem('refresh_token');
        navigate('/login');
      }
    } catch (error) {
      console.log(error);
      localStorage.removeItem('token');
      localStorage.removeItem('refresh_token');
      navigate('/login');
    }
  }

  const data = { login, logout, isAuth, token, setIsAuth,getNewAccessToken };
  return <AuthContext.Provider value={data}>{children}</AuthContext.Provider>;
};

export default AuthContext;
