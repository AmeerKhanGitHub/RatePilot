import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import LoanForm from '../LoanForm';

test('renders LoanForm with input fields and calculate button', () => {
    render(<LoanForm onSubmit={() => {}} />);

    expect(screen.getByLabelText(/Maturity Date/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Rate Floor/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Rate Ceiling/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Rate Spread/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Calculate/i })).toBeInTheDocument();
});

test('submits the form with valid input values', () => {
    const onSubmit = jest.fn();

    render(<LoanForm onSubmit={onSubmit} />);

    fireEvent.change(screen.getByLabelText(/Maturity Date/i), { target: { value: '2023-12-31' } });
    fireEvent.change(screen.getByLabelText(/Rate Floor/i), { target: { value: '0.01' } });
    fireEvent.change(screen.getByLabelText(/Rate Ceiling/i), { target: { value: '0.05' } });
    fireEvent.change(screen.getByLabelText(/Rate Spread/i), { target: { value: '0.02' } });
    fireEvent.click(screen.getByRole('button', { name: /Calculate/i }));

    expect(onSubmit).toHaveBeenCalledWith({
        maturity_date: '12/31/2023',
        reference_rate: 'SOFR',
        rate_floor: 0.01,
        rate_ceiling: 0.05,
        rate_spread: 0.02,
    });
});

test('displays alert on invalid numeric input', () => {
    global.alert = jest.fn();

    render(<LoanForm onSubmit={() => {}} />);

    fireEvent.change(screen.getByLabelText(/Rate Floor/i), { target: { value: 'invalid' } });
    fireEvent.click(screen.getByRole('button', { name: /Calculate/i }));

    expect(global.alert).toHaveBeenCalledWith("Please enter valid numeric values for the rates.");
});
