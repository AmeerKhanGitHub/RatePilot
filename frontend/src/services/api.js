import axios from 'axios';

export const instance = axios.create({
    baseURL: 'http://localhost:5000',
});

export const calculateRates = async loanDetails => {
    try {
        const response = await instance.post('/api/calculate-rates', loanDetails, {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching rates:', error);
        throw error;
    }
};
