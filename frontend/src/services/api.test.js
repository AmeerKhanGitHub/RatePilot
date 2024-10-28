// Import axios and the function under test
const axios = require('axios');
const { calculateRates, instance } = require('./api');

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

test('posts loan details and returns calculated rates', async () => {
    const loanDetails = {
        maturity_date: '12/31/2023',
        rate_floor: 0.01,
        rate_ceiling: 0.05,
        rate_spread: 0.02,
    };

    const data = [{ date: '2023-01-01', rate: 0.015 }, { date: '2023-02-01', rate: 0.018 }];

    // Mock instance.post to return a successful response
    instance.post.mockResolvedValueOnce({ data });

    const result = await calculateRates(loanDetails);

    expect(result).toEqual(data);
    expect(instance.post).toHaveBeenCalledWith('/api/calculate-rates', loanDetails, {
        headers: { 'Content-Type': 'application/json' },
    });
});

test('handles network errors gracefully', async () => {
    const loanDetails = {
        maturity_date: '12/31/2023',
        rate_floor: 0.01,
        rate_ceiling: 0.05,
        rate_spread: 0.02,
    };

    // Mock instance.post to simulate a network error
    instance.post.mockRejectedValueOnce(new Error('Network Error'));

    await expect(calculateRates(loanDetails)).rejects.toThrow('Network Error');
});
