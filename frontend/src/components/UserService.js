import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import AuthGuard from './AuthGuard';

const UserService = () => {
    const { user, logout } = useAuth();
    const [userInfo, setUserInfo] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchUserInfo = async () => {
            if (!user) return;
            
            try {
                const response = await fetch(`${process.env.REACT_APP_USER_SERVICE_URL}/api/users/${user.backendId}`);
                if (!response.ok) {
                    throw new Error(`Failed to fetch user information: ${response.status}`);
                }
                const data = await response.json();
                setUserInfo(data);
                setError(null); // Clear any previous errors
            } catch (error) {
                console.error('Error fetching user info:', error);
                setError('Failed to load user information. Please try again later.');
                // Set fallback user info from Firebase user
                setUserInfo({
                    id: user.backendId,
                    username: user.username || user.displayName || 'N/A',
                    email: user.email
                });
            } finally {
                setLoading(false);
            }
        };

        fetchUserInfo();
    }, [user]);

    const UserContent = () => {
        if (loading) {
            return <p>Loading user information...</p>;
        }

        if (error) {
            return <p style={{ color: 'red' }}>{error}</p>;
        }

        return (
            <div style={{ maxWidth: '600px', margin: '2rem auto', padding: '2rem', border: '1px solid #ddd', borderRadius: '8px' }}>
                <h2>My Account</h2>
                <div style={{ marginBottom: '1rem' }}>
                    <strong>User ID:</strong> {userInfo?.id || user.backendId}
                </div>
                <div style={{ marginBottom: '1rem' }}>
                    <strong>Username:</strong> {userInfo?.username || user.username || 'N/A'}
                </div>
                <div style={{ marginBottom: '1rem' }}>
                    <strong>Email:</strong> {userInfo?.email || user.email}
                </div>
                <div style={{ marginBottom: '1rem' }}>
                    <strong>Firebase UID:</strong> {user.uid}
                </div>
                <button 
                    onClick={logout}
                    style={{ 
                        padding: '0.75rem 1.5rem', 
                        backgroundColor: '#dc3545', 
                        color: 'white', 
                        border: 'none', 
                        borderRadius: '4px', 
                        cursor: 'pointer',
                        fontSize: '1rem'
                    }}
                >
                    Logout
                </button>
            </div>
        );
    };

    return (
        <AuthGuard>
            <UserContent />
        </AuthGuard>
    );
};

export default UserService;
