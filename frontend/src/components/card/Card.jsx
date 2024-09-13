import React, { useState, useEffect } from "react";
import "./Card.css";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';
import { useTheme } from '../../contexts/ThemeContext'; // Import your theme context

ChartJS.register(ArcElement, Tooltip, Legend);

const Card = ({ title, description, type }) => {
  const { theme } = useTheme(); // Access the current theme
  const [count, setCount] = useState(0);
  const [chartData, setChartData] = useState({
    labels: ['Positive', 'Negative', 'Neutral'],
    datasets: [{
      data: [33, 33, 34],
      backgroundColor: ['#36A2EB', '#FF6384', '#FFCE56']
    }]
  });

  useEffect(() => {
    if (type === 'counter') {
      const interval = setInterval(() => {
        setCount(prevCount => prevCount + Math.floor(Math.random() * 5));
      }, 5000);
      return () => clearInterval(interval);
    }

    if (type === 'chart') {
      const interval = setInterval(() => {
        setChartData(prevData => ({
          ...prevData,
          datasets: [{
            ...prevData.datasets[0],
            data: [
              Math.floor(Math.random() * 100),
              Math.floor(Math.random() * 100),
              Math.floor(Math.random() * 100)
            ]
          }]
        }));
      }, 5000);
      return () => clearInterval(interval);
    }
  }, [type]);

  return (
    <div className={`card card-${theme}`}> {/* Apply the theme class */}
      <h3>{title}</h3>
      {type === 'counter' && <p>{count}</p>}
      {type === 'chart' && <Pie data={chartData} />}
      {!type && <p>{description}</p>}
    </div>
  );
};

export default Card;
