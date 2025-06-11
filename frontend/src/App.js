// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';

import Tasks from './components/Tasks';
import UserService from './components/UserService';
import NotificationService from './components/NotificationService';
import DonationService from './components/DonationService';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Login from './components/Login';
import './App.css';

const AppContent = () => {
  const { loading } = useAuth();

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <div>Loading...</div>
      </div>
    );
  }

  return (
    <>
      <Navbar />
      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/tasks" element={<Tasks />} />
          <Route path="/users" element={<UserService />} />
          <Route path="/notifications" element={<NotificationService />} />
          <Route path="/donations" element={<DonationService />} />
        </Routes>
      </div>
    </>
  );
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
}

export default App;
