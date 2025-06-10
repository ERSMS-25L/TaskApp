// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Transactions from './components/Transactions';
import UserService from './components/UserService';
import NotificationService from './components/NotificationService';
import Navbar from './components/Navbar';
import Home from './components/Home'; // Import Home component
import './App.css';

function App() {
  return (
    <Router>
      <Navbar />
      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} /> {/* Home component as default */}
          <Route path="/transactions" element={<Transactions />} />
          <Route path="/users" element={<UserService />} />
          <Route path="/notifications" element={<NotificationService />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
