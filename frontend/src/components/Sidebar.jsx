// src/components/Sidebar.jsx
import React from "react";
import "./Sidebar.css";
import logo from "../assets/ecitizen.png";
import { useTheme } from "../contexts/ThemeContext"; // Import the useTheme hook

const Sidebar = () => {
  const { currentTheme } = useTheme(); // Use the useTheme hook to get the current theme

  return (
    <div className={`sidebar ${currentTheme}`}> {/* Add currentTheme as a class */}
      <img src={logo} alt="Logo" className="logo" />
      <ul>
        <li>
          <a href="#">Home</a>
        </li>
        <li>
          <a href="#">Users</a>
        </li>
        <li>
          <a href="#">Form</a>
        </li>
        <li>
          <a href="#">Change Password</a>
        </li>
        <li>
          <a href="#">Logout</a>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;