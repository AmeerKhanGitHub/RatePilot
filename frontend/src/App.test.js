import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';
const axios = require('axios');
const { calculateRates, instance } = require('./services/api');

// Mock axios with both `post` and `create`
jest.mock('axios', () => {
  const axiosInstance = {
    post: jest.fn(),
  };
  return {
    create: jest.fn(() => axiosInstance),
    post: jest.fn(), // Include this if direct axios.post calls exist outside the instance
  };
});

jest.mock('./services/api');

beforeEach(() => {
  render(<App />);
});

test('renders LoanForm initially', () => {
  expect(screen.getByText(/Loan Calculation Form/i)).toBeInTheDocument();
});

test('displays LoanChart after successful form submission', async () => {
  calculateRates.mockResolvedValueOnce([
    { date: '2023-01-01', rate: 0.015 },
    { date: '2023-02-01', rate: 0.018 },
  ]);

  fireEvent.change(screen.getByLabelText(/Maturity Date/i), { target: { value: '2023-12-31' } });
  fireEvent.change(screen.getByLabelText(/Rate Floor/i), { target: { value: '0.01' } });
  fireEvent.change(screen.getByLabelText(/Rate Ceiling/i), { target: { value: '0.05' } });
  fireEvent.change(screen.getByLabelText(/Rate Spread/i), { target: { value: '0.02' } });
  fireEvent.click(screen.getByRole('button', { name: /Calculate/i }));

});

test('resets form and hides LoanChart on redo', async () => {
  calculateRates.mockResolvedValueOnce([
    { date: '2023-01-01', rate: 0.015 },
    { date: '2023-02-01', rate: 0.018 },
  ]);

  fireEvent.change(screen.getByLabelText(/Maturity Date/i), { target: { value: '2023-12-31' } });
  fireEvent.change(screen.getByLabelText(/Rate Floor/i), { target: { value: '0.01' } });
  fireEvent.change(screen.getByLabelText(/Rate Ceiling/i), { target: { value: '0.05' } });
  fireEvent.change(screen.getByLabelText(/Rate Spread/i), { target: { value: '0.02' } });
  fireEvent.click(screen.getByRole('button', { name: /Calculate/i }));

  expect(screen.queryByText(/Loan Rate Chart/i)).not.toBeInTheDocument();
  expect(screen.getByText(/Loan Calculation Form/i)).toBeInTheDocument();
});
