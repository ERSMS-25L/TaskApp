// src/components/Home.js
import React from 'react';

const Home = () => {
    return (
        <div style={{ padding: '20px', textAlign: 'center' }}>
            <h2>Welcome to the Task Dashboard</h2>
            <p>This sample app lets you manage tasks using a microservice architecture.</p>
            <p>Available services:</p>
            <ul style={{ listStyleType: 'none', padding: '0' }}>
                <li>✅ Task Service</li>
                <li>👥 User Service</li>
                <li>🔔 Notification Service</li>
            </ul>
            <p>Use the navigation bar above to access each section.</p>
        </div>
    );
};

export default Home;
