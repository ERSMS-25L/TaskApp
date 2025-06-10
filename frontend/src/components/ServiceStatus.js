// src/components/ServiceStatus.js
import React, { useEffect, useState } from 'react';
import './ServiceStatus.css'; // Assuming you create a separate CSS file for styling

const ServiceStatus = () => {
    const [serviceStatus, setServiceStatus] = useState({
        userService: '',
        transactionService: '',
        notificationService: ''
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkServiceStatus = async () => {
            try {
                // Fetch service health check endpoints using environment variables
                const userResponse = await fetch(`${process.env.REACT_APP_USER_SERVICE_URL}/api/health`);
                const transactionResponse = await fetch(`${process.env.REACT_APP_TRANSACTION_SERVICE_URL}/api/health`);
                const notificationResponse = await fetch(`${process.env.REACT_APP_NOTIFICATION_SERVICE_URL}/api/health`);

                // Check if the responses are OK (status code 200)
                const userStatus = userResponse.ok ? 'running' : 'OFF';
                const transactionStatus = transactionResponse.ok ? 'running' : 'OFF';
                const notificationStatus = notificationResponse.ok ? 'running' : 'OFF';

                setServiceStatus({
                    userService: userStatus,
                    transactionService: transactionStatus,
                    notificationService: notificationStatus,
                });
            } catch (error) {
                console.error('Error fetching service status:', error);
                setServiceStatus({
                    userService: 'Error',
                    transactionService: 'Error',
                    notificationService: 'Error',
                });
            } finally {
                setLoading(false); // Stop loading once the status is checked
            }
        };

        checkServiceStatus();
    }, []);

    const getStatusClass = (status) => {
        if (status === 'running') return 'status-running';
        if (status === 'Error') return 'status-error';
        return 'status-unknown';
    };

    const createServiceLink = (serviceName) => {
        switch (serviceName) {
            case 'userService':
                return process.env.REACT_APP_USER_SERVICE_URL; // Use environment variable
            case 'transactionService':
                return process.env.REACT_APP_TRANSACTION_SERVICE_URL; // Use environment variable
            case 'notificationService':
                return process.env.REACT_APP_NOTIFICATION_SERVICE_URL; // Use environment variable
            default:
                return '#';
        }
    };

    const getHealthStatus = (status) => {
        return status === 'running' ? 'ON' : 'OFF';
    };

    return (
        <div className="service-status-container">
            <h2>Service Status</h2>
            {loading ? (
                <p>Loading service status...</p>
            ) : (
                <table className="service-status-table">
                    <thead>
                        <tr>
                            <th>Service</th>
                            <th>Status</th>
                            <th>Health Check</th>
                            <th>View Service</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Object.entries(serviceStatus).map(([service, status]) => (
                            <tr key={service} className={getStatusClass(status)}>
                                <td>{service.replace(/([A-Z])/g, ' $1')}</td>
                                <td>{status === 'running' ? `${service.replace(/([A-Z])/g, ' $1')} is running!` : status}</td>
                                <td>{getHealthStatus(status)}</td> {/* Display ON or OFF */}
                                <td>
                                    <a
                                        href={createServiceLink(service)}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="service-link"
                                    >
                                        (Open Service)
                                    </a>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default ServiceStatus;
