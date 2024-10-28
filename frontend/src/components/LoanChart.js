import { useEffect, useRef, useState } from 'react';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

const LoanChart = ({ chartData, rateFloor, rateCeiling, onRedo }) => {
    const chartRef = useRef(null);
    const [isPercentage, setIsPercentage] = useState(false);
    let myChart = null;

    const toggleFormat = () => setIsPercentage(prev => !prev);
    const formatData = data => data.map(value => (isPercentage ? value * 100 : value));

    useEffect(() => {
        if (chartRef.current) {
            const ctx = chartRef.current.getContext('2d');
            if (myChart) myChart.destroy();

            myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: chartData.labels,
                    datasets: [
                        ...chartData.datasets.map(dataset => ({
                            ...dataset,
                            data: formatData(dataset.data),
                        })),
                        {
                            label: 'Rate Floor',
                            data: Array(chartData.labels.length).fill(isPercentage ? rateFloor * 100 : rateFloor),
                            borderColor: 'red',
                            borderDash: [5, 5],
                            pointRadius: 0,
                            fill: false,
                        },
                        {
                            label: 'Rate Ceiling',
                            data: Array(chartData.labels.length).fill(isPercentage ? rateCeiling * 100 : rateCeiling),
                            borderColor: 'blue',
                            borderDash: [5, 5],
                            pointRadius: 0,
                            fill: false,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'top' },
                        title: { display: true, text: 'Loan Rate Chart' },
                    },
                },
            });
        }

        return () => {
            if (myChart) myChart.destroy();
        };
    }, [chartData, rateFloor, rateCeiling, isPercentage]);

    return (
        <div style={{ position: 'relative', padding: '20px', textAlign: 'center', maxWidth: '900px', margin: '0 auto' }}>
            <button onClick={toggleFormat} style={{ marginBottom: '10px', padding: '10px', backgroundColor: 'lightgray', border: 'none', cursor: 'pointer', position: 'absolute', left: '20px' }}>
                Switch to {isPercentage ? 'Decimal' : 'Percentage'}
            </button>
            <button onClick={onRedo} style={{ position: 'absolute', top: '10px', right: '10px', backgroundColor: '#4CAF50', color: '#fff', border: 'none', borderRadius: '5px', cursor: 'pointer', padding: '5px 10px' }}>
                &#x21B6;
            </button>
            <canvas ref={chartRef} style={{ width: '100%', height: '400px' }}></canvas>
        </div>
    );
};

export default LoanChart;
