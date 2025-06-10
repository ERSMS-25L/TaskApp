// src/components/Navbar.js
import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'; // Import the CSS file for styling

const Navbar = () => {
    return (
        <nav className="navbar">
            <h1 className="navbar-title">Finance Dashboard</h1> {/* Add a title */}
            <ul className="navbar-links">
                <li>
                    <Link to="/transactions">Transactions</Link>
                </li>
                <li>
                    <Link to="/users">Users</Link> {/* Link to UserService */}
                </li>
                <li>
                    <Link to="/notifications">Notification</Link> {/* Link to NotificationService */}
                </li>
            </ul>
        </nav>
    );
};

export default Navbar;
