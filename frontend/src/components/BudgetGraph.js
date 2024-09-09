import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Pie } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
} from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const BudgetGraph = () => {
    const [budgetData, setBudgetData] = useState({});
    const [newLimit, setNewLimit] = useState('');
    const [purchaseAmount, setPurchaseAmount] = useState('');
    const [month, setMonth] = useState(new Date().getMonth() + 1);
    const [year, setYear] = useState(new Date().getFullYear());

    useEffect(() => {
        fetchBudgetData();
    }, [month, year]);

    const fetchBudgetData = () => {
        axios.get(`http://127.0.0.1:8000/budget/get_budget/?month=${month}&year=${year}`)
            .then(response => {
                setBudgetData(response.data);
            })
            .catch(error => {
                console.error('There was an error fetching the budget data!', error);
            });
    };

    const handleLimitChange = () => {
        axios.post('http://127.0.0.1:8000/budget/update_budget_limit/', { limit: newLimit })
            .then(response => {
                fetchBudgetData();
            })
            .catch(error => {
                console.error('There was an error updating the budget limit!', error);
            });
    };

    const handlePurchase = () => {
        axios.post('http://127.0.0.1:8000/budget/add_purchase/', { amount: purchaseAmount })
            .then(response => {
                fetchBudgetData();
            })
            .catch(error => {
                console.error('There was an error adding the purchase!', error);
            });
    };

    const data = {
        labels: ['Spent', 'Remaining'],
        datasets: [
            {
                label: 'Budget',
                data: [budgetData.current_month_spent, budgetData.limit - budgetData.current_month_spent],
                backgroundColor: ['rgb(255, 99, 132)', 'rgb(54, 162, 235)'],
                hoverOffset: 4,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
            },
        },
    };

    return (
        <div>
            <h2>Budget Graph</h2>
            <div>
                <label>
                    New Budget Limit:
                    <input type="number" value={newLimit} onChange={(e) => setNewLimit(e.target.value)} />
                </label>
                <button onClick={handleLimitChange}>Update Limit</button>
            </div>
            <div>
                <label>
                    Purchase Amount:
                    <input type="number" value={purchaseAmount} onChange={(e) => setPurchaseAmount(e.target.value)} />
                </label>
                <button onClick={handlePurchase}>Add Purchase</button>
            </div>
            <div>
                <label>
                    Month:
                    <input type="number" value={month} onChange={(e) => setMonth(e.target.value)} />
                </label>
                <label>
                    Year:
                    <input type="number" value={year} onChange={(e) => setYear(e.target.value)} />
                </label>
                <button onClick={fetchBudgetData}>Fetch Data</button>
            </div>
            <div style={{ width: '50%', height: '50%' }}>
                <Pie data={data} options={options} />
            </div>
        </div>
    );
};

export default BudgetGraph;
