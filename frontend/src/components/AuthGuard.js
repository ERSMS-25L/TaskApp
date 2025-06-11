import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const AuthGuard = ({ children }) => {
  const { user, loading } = useAuth();
  const navigate = useNavigate();

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return (
      <div style={{ textAlign: 'center', padding: '2rem' }}>
        <h2>Authentication Required</h2>
        <p>You need to be logged in to access this content.</p>
        <button 
          onClick={() => navigate('/login')}
          style={{ 
            padding: '0.75rem 1.5rem', 
            backgroundColor: '#007bff', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px', 
            cursor: 'pointer',
            fontSize: '1rem'
          }}
        >
          Go to Login
        </button>
      </div>
    );
  }

  return children;
};

export default AuthGuard;
