// src/components/Dashboard.jsx
import React from 'react';
import Card from './card/Card';

const Dashboard = () => {
  return (
    <section className="cards" style={{ display: 'flex', flexGrow: 1, flexWrap: 'wrap', gap: '1rem' }}>
      <Card
        title="Daily Users"
        description="Number of users that have interacted with system today."
        type="counter"
      />
      <Card
        title="Message Hits"
        description="Today's Messages."
        type="counter"
      />
      <Card
        title="FAQs"
        description="Most frequently asked questions."
      />
      <Card
        title="Comment Chart"
        description="Satisfaction distribution"
        type="chart"
      />
    </section>
  );
};

export default Dashboard;
