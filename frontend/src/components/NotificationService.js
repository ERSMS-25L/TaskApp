// src/components/NotificationService.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './ServiceStatus.css'; // Reuse styling for consistency

const NotificationService = () => {
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState(null);
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    const fetchServiceStatus = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_NOTIFICATION_SERVICE_URL}/api/health`);
        setStatus(response.data.status === "Notification Service is running!" ? "Success" : "Error");
      } catch (err) {
        setStatus("Error");
        setError(err);
      }
    };

    const fetchNotifications = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_NOTIFICATION_SERVICE_URL}/notifications`);
        setNotifications(response.data);
      } catch (err) {
        setError(err);
      }
    };

    fetchServiceStatus();
    fetchNotifications();
  }, []);

  return (
    <div className="service-status">
      <h2>Notification Service Status</h2>
      {status === 'loading' ? (
        <div>Loading service status...</div>
      ) : status === 'Error' ? (
        <div className="error-message">Error: {error ? error.message : "Notification Service is down"}</div>
      ) : (
        <div className="success-message">Notification Service is up and running!</div>
      )}

      <h3>Recent Notifications</h3>
      {notifications.length > 0 ? (
        <table className="notification-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Message</th>
              <th>Recipient</th>
              <th>Type</th>
            </tr>
          </thead>
          <tbody>
            {notifications.map(notification => (
              <tr key={notification.id}>
                <td>{notification.id}</td>
                <td>{notification.message}</td>
                <td>{notification.recipient}</td>
                <td>{notification.notification_type}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <div>No notifications available</div>
      )}
    </div>
  );
};

export default NotificationService;
