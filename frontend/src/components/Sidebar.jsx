// src/components/Sidebar.jsx
import React from "react";
import { Link } from "react-router-dom";
import "./Sidebar.css";
import logo from "../assets/logo.svg";
import { useTheme } from "../contexts/ThemeContext";

const Sidebar = () => {
  const { currentTheme } = useTheme();

  return (
    <div className={`sidebar ${currentTheme}`}>
      <img src={logo} alt="Logo" className="logo" />
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/form">Form</Link>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;
