// src/Footer.js

import React from 'react';
import './Footer.css'; // optional: for styling your footer
import { useTheme } from '../../contexts/ThemeContext';

const Footer = () => {
  const { theme } = useTheme();
  return (
    <footer className={`footer footer-${theme}`}>
      <p>&copy; Directorate of eCitizen 2024. All rights reserved.</p>
    </footer>
  );
};

export default Footer;
