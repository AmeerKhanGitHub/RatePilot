import React, { useState } from 'react';

const LoanForm = ({ onSubmit }) => {
    const [formData, setFormData] = useState({
        maturity_date: '',
        rate_floor: '',
        rate_ceiling: '',
        rate_spread: '',
    });

    const handleChange = e => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = e => {
        e.preventDefault();
        const { maturity_date, rate_floor, rate_ceiling, rate_spread } = formData;

        if (isNaN(rate_floor) || isNaN(rate_ceiling) || isNaN(rate_spread)) {
            alert("Please enter valid numeric values for the rates.");
            return;
        }

        const [year, month, day] = maturity_date.split('-');
        const formattedData = {
            maturity_date: `${month}/${day}/${year}`,
            reference_rate: 'SOFR',
            rate_floor: parseFloat(rate_floor),
            rate_ceiling: parseFloat(rate_ceiling),
            rate_spread: parseFloat(rate_spread),
        };

        onSubmit(formattedData);
    };

    return (
        <div style={{ maxWidth: '600px', margin: '20px auto', padding: '30px', borderRadius: '8px', boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.1)', backgroundColor: '#f9f9f9' }}>
            <h2 style={{ textAlign: 'center', marginBottom: '20px', color: '#333' }}>Loan Calculation Form</h2>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column' }}>
                <label style={{ marginBottom: '10px' }}>
                    Maturity Date:
                    <input type="date" name="maturity_date" value={formData.maturity_date} onChange={handleChange} required style={{ width: '100%', padding: '10px', marginTop: '5px', borderRadius: '4px', border: '1px solid #ccc' }} />
                </label>
                <label style={{ marginBottom: '10px' }}>
                    Rate Floor:
                    <input type="text" name="rate_floor" placeholder="e.g., 0.02" value={formData.rate_floor} onChange={handleChange} required style={{ width: '100%', padding: '10px', marginTop: '5px', borderRadius: '4px', border: '1px solid #ccc' }} />
                </label>
                <label style={{ marginBottom: '10px' }}>
                    Rate Ceiling:
                    <input type="text" name="rate_ceiling" placeholder="e.g., 0.2" value={formData.rate_ceiling} onChange={handleChange} required style={{ width: '100%', padding: '10px', marginTop: '5px', borderRadius: '4px', border: '1px solid #ccc' }} />
                </label>
                <label style={{ marginBottom: '10px' }}>
                    Rate Spread:
                    <input type="text" name="rate_spread" placeholder="e.g., 0.01" value={formData.rate_spread} onChange={handleChange} required style={{ width: '100%', padding: '10px', marginTop: '5px', borderRadius: '4px', border: '1px solid #ccc' }} />
                </label>
                <button type="submit" style={{ padding: '10px', marginTop: '15px', borderRadius: '4px', border: 'none', backgroundColor: '#4CAF50', color: '#fff', cursor: 'pointer', fontSize: '16px' }}>
                    Calculate
                </button>
            </form>
        </div>
    );
};

export default LoanForm;
