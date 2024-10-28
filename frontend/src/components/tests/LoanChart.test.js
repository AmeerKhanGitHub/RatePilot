import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import LoanChart from '../LoanChart';

test('renders LoanChart with chart and buttons', () => {
    const chartData = {
        labels: ['Jan', 'Feb', 'Mar'],
        datasets: [{ label: 'Rate', data: [0.01, 0.02, 0.03] }],
    };

    render(<LoanChart chartData={chartData} rateFloor={0.01} rateCeiling={0.03} onRedo={() => {}} />);

    expect(screen.getByRole('button', { name: /Switch to/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /↶/i })).toBeInTheDocument();
});

test('toggles between percentage and decimal format', () => {
    const chartData = {
        labels: ['Jan', 'Feb', 'Mar'],
        datasets: [{ label: 'Rate', data: [0.01, 0.02, 0.03] }],
    };

    render(<LoanChart chartData={chartData} rateFloor={0.01} rateCeiling={0.03} onRedo={() => {}} />);

    const button = screen.getByRole('button', { name: /Switch to/i });
    expect(button).toBeInTheDocument();

    // Simulating clicks to toggle format
    fireEvent.click(button);
    fireEvent.click(button);
});
