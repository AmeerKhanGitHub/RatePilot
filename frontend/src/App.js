import React, { useState } from 'react';
import LoanForm from '../src/components/LoanForm';
import LoanChart from '../src/components/LoanChart';
import { calculateRates } from '../src/services/api';

function App() {
    const [chartData, setChartData] = useState(null);
    const [rateFloor, setRateFloor] = useState(null);
    const [rateCeiling, setRateCeiling] = useState(null);
    const [showChart, setShowChart] = useState(false);

    const handleFormSubmit = async formData => {
        try {
            const result = await calculateRates(formData);

            const labels = result.map(item => item.date);
            const data = result.map(item => item.rate);

            setChartData({
                labels,
                datasets: [{
                    label: 'Interest Rate (%)',
                    data,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1,
                    fill: false,
                }]
            });

            setRateFloor(formData.rate_floor);
            setRateCeiling(formData.rate_ceiling);
            setShowChart(true);
        } catch (error) {
            console.error("Error fetching rates:", error);
        }
    };

    const handleRedo = () => {
        setShowChart(false);
        setChartData(null);
    };

    return (
        <div className="App">
            {!showChart ? <LoanForm onSubmit={handleFormSubmit} /> : <LoanChart chartData={chartData} rateFloor={rateFloor} rateCeiling={rateCeiling} onRedo={handleRedo} />}
        </div>
    );
}

export default App;
