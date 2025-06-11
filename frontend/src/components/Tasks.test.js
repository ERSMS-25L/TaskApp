import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import axios from 'axios';
import Tasks from './Tasks';

jest.mock('axios');

test('displays tasks from API', async () => {
  axios.get.mockResolvedValue({ data: [{ id: 1, title: 'Test', completed: false }] });
  render(<Tasks />);
  expect(screen.getByText(/Loading tasks/)).toBeInTheDocument();
  await waitFor(() => screen.getByText('Test'));
});
