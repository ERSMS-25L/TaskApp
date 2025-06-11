// src/components/DonationService.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './ServiceStatus.css'; // Reuse styling for consistency

const DonationService = () => {
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState(null);
  const [donationForm, setDonationForm] = useState({
    amount: 10,
    currency: 'usd',
    donor_email: '',
    donor_name: '',
    description: 'Donation'
  });
  const [isCreatingPayment, setIsCreatingPayment] = useState(false);
  const [charityLinks, setCharityLinks] = useState([]);
  const [isLoadingCharities, setIsLoadingCharities] = useState(false);

  useEffect(() => {
    const fetchServiceStatus = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_DONATION_SERVICE_URL}/api/health`);
        setStatus(response.data.status === "Donation Service is running!" ? "Success" : "Error");
      } catch (err) {
        setStatus("Error");
        setError(err);
      }
    };

    const fetchCharityLinks = async () => {
      setIsLoadingCharities(true);
      try {
        const response = await axios.get(`${process.env.REACT_APP_DONATION_SERVICE_URL}/get-charity-links`);
        setCharityLinks(response.data);
      } catch (err) {
        console.error('Error fetching charity links:', err);
        setCharityLinks([]);
      } finally {
        setIsLoadingCharities(false);
      }
    };

    fetchServiceStatus();
    fetchCharityLinks();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setDonationForm(prev => ({
      ...prev,
      [name]: name === 'amount' ? parseInt(value * 100) : value // Convert dollars to cents
    }));
  };

  const handleDonationSubmit = async (e) => {
    e.preventDefault();
    setIsCreatingPayment(true);
    
    try {
      const response = await axios.post(`${process.env.REACT_APP_DONATION_SERVICE_URL}/donate`, donationForm);
      
      // Redirect to Stripe payment page
      window.location.href = response.data.payment_url;
    } catch (err) {
      setError(err);
      alert('Error creating donation link: ' + (err.response?.data?.detail || err.message));
    } finally {
      setIsCreatingPayment(false);
    }
  };

  return (
    <div className="service-status">
      <h2>Donation Service Status</h2>
      {status === 'loading' ? (
        <div>Loading service status...</div>
      ) : status === 'Error' ? (
        <div className="error-message">Error: {error ? error.message : "Donation Service is down"}</div>
      ) : (
        <div className="success-message">Donation Service is up and running!</div>
      )}

      <div className="donation-form-container">
        <h3>Make a Donation</h3>
        <form onSubmit={handleDonationSubmit} className="donation-form">
          <div className="form-group">
            <label htmlFor="amount">Amount ($):</label>
            <input
              type="number"
              id="amount"
              name="amount"
              value={donationForm.amount / 100}
              onChange={handleInputChange}
              min="1"
              step="0.01"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="donor_name">Your Name (optional):</label>
            <input
              type="text"
              id="donor_name"
              name="donor_name"
              value={donationForm.donor_name}
              onChange={handleInputChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="donor_email">Your Email (optional):</label>
            <input
              type="email"
              id="donor_email"
              name="donor_email"
              value={donationForm.donor_email}
              onChange={handleInputChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Description:</label>
            <input
              type="text"
              id="description"
              name="description"
              value={donationForm.description}
              onChange={handleInputChange}
            />
          </div>

          <button 
            type="submit" 
            disabled={isCreatingPayment}
            className="donation-button"
          >
            {isCreatingPayment ? 'Creating Payment Link...' : 'Donate Now'}
          </button>
        </form>
      </div>

      <div className="charity-links-container">
        <h3>Donate to Charity</h3>
        {isLoadingCharities ? (
          <div>Loading charity links...</div>
        ) : charityLinks.length > 0 ? (
          <div className="charity-buttons">
            {charityLinks.map((charity, index) => (
              <button
                key={index}
                className="charity-button"
                onClick={() => window.open(charity.url, '_blank')}
              >
                {charity.name}
              </button>
            ))}
          </div>
        ) : (
          <div>No charity links available at the moment.</div>
        )}
      </div>
    </div>
  );
};

export default DonationService;
