import { render, screen } from '@testing-library/react';
jest.mock('./firebase', () => ({ auth: {} }));
jest.mock('firebase/auth', () => ({
  onAuthStateChanged: jest.fn(),
  signInWithEmailAndPassword: jest.fn(),
  signOut: jest.fn(),
  getAuth: jest.fn(),
}));
import App from './App';

test('renders navbar with Tasks link', () => {
  render(<App />);
  const links = screen.getAllByText(/Tasks/i);
  expect(links.length).toBeGreaterThan(0);
});
