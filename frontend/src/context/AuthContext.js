import React, { createContext, useContext, useState, useEffect } from 'react';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut, onAuthStateChanged } from 'firebase/auth';
import { auth } from '../firebase';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
      if (firebaseUser) {
        try {
          // Get Firebase ID token and verify with backend
          const token = await firebaseUser.getIdToken();
          const response = await axios.post(`${process.env.REACT_APP_USER_SERVICE_URL}/api/auth/verify`, {
            token: token
          });
          
          // Set user with backend user data
          setUser({
            ...firebaseUser,
            backendId: response.data.id,
            username: response.data.username
          });
        } catch (error) {
          console.error('Error verifying token with backend:', error);
          setUser(firebaseUser);
        }
      } else {
        setUser(null);
      }
      setLoading(false);
    });
    return unsubscribe;
  }, []);

  const login = (email, password) => signInWithEmailAndPassword(auth, email, password);
  
  const register = async (email, password, username) => {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    // The onAuthStateChanged listener will handle backend registration
    return userCredential;
  };
  
  const logout = () => signOut(auth);

  return (
    <AuthContext.Provider value={{ user, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
