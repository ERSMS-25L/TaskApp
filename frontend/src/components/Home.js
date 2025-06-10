// src/components/Home.js
import React from 'react';

const Home = () => {
    return (
        <div style={{ padding: '20px', textAlign: 'center' }}>
            <h2>Welcome to the Finance Dashboard</h2>
            <p>This is a sample finance application built with a microservice architecture.</p>
            <p>Explore the available services:</p>
            <ul style={{ listStyleType: 'none', padding: '0' }}>
                <li>💳 Transactions Service</li>
                <li>👥 User Service</li>
                <li>🔔 Notification Service</li>
            </ul>
            <p>Use the navigation bar above to access each service.</p>
        </div>
    );
};

export default Home;
