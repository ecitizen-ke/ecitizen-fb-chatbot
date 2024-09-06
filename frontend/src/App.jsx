import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import Home from './pages/Home';
import Login from './pages/login/Login';
import { AuthProvider } from './contexts/AuthContext';
import Chatbot from './components/Chatbot/chatbot';
import Dashboard from './components/Dashboard';

const App = () => {
  return (
    <ThemeProvider>
      <Router>
        <AuthProvider>
          <Routes>
            <Route path="/" element={<Home />}>
              <Route index element={<Dashboard />} />
              <Route path="form" element={<Chatbot />} />
            </Route>
            <Route path="/login" element={<Login />} />
          </Routes>
        </AuthProvider>
      </Router>
    </ThemeProvider>
  );
};

export default App;
