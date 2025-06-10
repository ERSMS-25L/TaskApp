-- Create Users
INSERT INTO users (username, email, password) VALUES
('user1', 'user1@example.com', 'password1'),
('user2', 'user2@example.com', 'password2'),
('user3', 'user3@example.com', 'password3');

-- Create Transactions
INSERT INTO transactions (user_id, amount, transaction_date) VALUES
(1, 100.00, '2024-11-01'),
(1, 150.00, '2024-11-02'),
(2, 200.00, '2024-11-01'),
(3, 300.00, '2024-11-03');

-- Create Notifications
INSERT INTO notifications (user_id, message, notification_date) VALUES
(1, 'Transaction successful', '2024-11-01'),
(2, 'Transaction failed', '2024-11-02'),
(3, 'Transaction pending', '2024-11-03');
