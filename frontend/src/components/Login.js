import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const { login, register, user } = useAuth();
  const navigate = useNavigate();
  const [isRegistering, setIsRegistering] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [error, setError] = useState(null);

  // Redirect if already logged in
  React.useEffect(() => {
    if (user) {
      navigate('/');
    }
  }, [user, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      if (isRegistering) {
        await register(email, password, username);
      } else {
        await login(email, password);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const toggleMode = () => {
    setIsRegistering(!isRegistering);
    setError(null);
    setUsername('');
  };

  return (
    <div style={{ maxWidth: '400px', margin: '2rem auto', padding: '2rem', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h2>{isRegistering ? 'Register' : 'Login'}</h2>
      <form onSubmit={handleSubmit}>
        {isRegistering && (
          <div style={{ marginBottom: '1rem' }}>
            <input 
              type="text" 
              value={username} 
              onChange={e => setUsername(e.target.value)} 
              placeholder="Username" 
              required 
              style={{ width: '100%', padding: '0.5rem', marginBottom: '0.5rem' }}
            />
          </div>
        )}
        <div style={{ marginBottom: '1rem' }}>
          <input 
            type="email" 
            value={email} 
            onChange={e => setEmail(e.target.value)} 
            placeholder="Email" 
            required 
            style={{ width: '100%', padding: '0.5rem' }}
          />
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <input 
            type="password" 
            value={password} 
            onChange={e => setPassword(e.target.value)} 
            placeholder="Password" 
            required 
            style={{ width: '100%', padding: '0.5rem' }}
          />
        </div>
        <button 
          type="submit" 
          style={{ width: '100%', padding: '0.75rem', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          {isRegistering ? 'Register' : 'Login'}
        </button>
      </form>
      
      <div style={{ marginTop: '1rem', textAlign: 'center' }}>
        <button 
          type="button" 
          onClick={toggleMode}
          style={{ background: 'none', border: 'none', color: '#007bff', textDecoration: 'underline', cursor: 'pointer' }}
        >
          {isRegistering ? 'Already have an account? Login' : "Don't have an account? Register"}
        </button>
      </div>
      
      {error && <p style={{ color: 'red', marginTop: '1rem' }}>{error}</p>}
    </div>
  );
};

export default Login;
