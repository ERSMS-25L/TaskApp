// src/components/Navbar.js
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css'; // Import the CSS file for styling

const Navbar = () => {
    const { user, logout } = useAuth();
    return (
        <nav className="navbar">
            <h1 className="navbar-title">Task Dashboard</h1>
            <ul className="navbar-links">
                <li>
                    <Link to="/tasks">Tasks</Link>
                </li>
                <li>
                    <Link to="/users">Users</Link>
                </li>
                <li>
                    <Link to="/notifications">Notification</Link>
                </li>
                {user ? (
                    <li><button onClick={logout}>Logout</button></li>
                ) : (
                    <li>
                        <Link to="/login">Login</Link>
                    </li>
                )}
                <li>
                    <Link to="/donations">Donations</Link> {/* Link to DonationService */}
                </li>
            </ul>
        </nav>
    );
};

export default Navbar;
