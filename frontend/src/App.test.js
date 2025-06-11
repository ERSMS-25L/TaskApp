import { render, screen } from '@testing-library/react';
import App from './App';

test('renders navbar with Tasks link', () => {
  render(<App />);
  const links = screen.getAllByText(/Tasks/i);
  expect(links.length).toBeGreaterThan(0);
});
