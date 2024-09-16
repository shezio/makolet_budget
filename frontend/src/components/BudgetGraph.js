import React, { useEffect, useState, useCallback } from 'react';
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
    const [errors, setErrors] = useState({});
    const [popupMessage, setPopupMessage] = useState('');

    const fetchBudgetData = useCallback(() => {
        axios.get(`http://127.0.0.1:8000/budget/get_budget/?month=${month}&year=${year}`)
            .then(response => {
                console.log('Budget Data:', response.data); // Debugging line
                setBudgetData(response.data);
            })
            .catch(error => {
                console.error('There was an error fetching the budget data!', error);
            });
    }, [month, year]);

    useEffect(() => {
        fetchBudgetData();
    }, [month, year, fetchBudgetData]);

    const validateLimit = () => {
        const newErrors = {};
        if (newLimit !== '' && newLimit <= 0) {
            newErrors.newLimit = 'Budget limit must be a positive number.';
        }
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const validatePurchase = () => {
        const newErrors = {};
        if (purchaseAmount === '' || isNaN(purchaseAmount)) {
            newErrors.purchaseAmount = 'Purchase amount must be a number.';
        } else if (purchaseAmount < 0 && Math.abs(purchaseAmount) > budgetData.current_month_spent) {
            newErrors.purchaseAmount = 'Cannot reduce spent amount below zero.';
        }
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleLimitChange = () => {
        setErrors({});
        setPopupMessage('');
        if (validateLimit()) {
            axios.post('http://127.0.0.1:8000/budget/update_budget_limit/', { limit: newLimit, month, year })
                .then(response => {
                    fetchBudgetData();
                })
                .catch(error => {
                    if (error.response && error.response.data && error.response.data.error) {
                        setPopupMessage(error.response.data.error);
                    } else {
                        console.error('There was an error updating the budget limit!', error);
                    }
                });
        }
    };

    const handlePurchase = () => {
        setErrors({});
        setPopupMessage('');
        if (validatePurchase()) {
            axios.post('http://127.0.0.1:8000/budget/add_purchase/', { amount: purchaseAmount, date: `${year}-${month}-01` })
                .then(response => {
                    fetchBudgetData();
                })
                .catch(error => {
                    if (error.response && error.response.data && error.response.data.error) {
                        setPopupMessage(error.response.data.error);
                    } else {
                        console.error('There was an error adding the purchase!', error);
                    }
                });
        }
    };

    const data = {
        labels: ['Spent', 'Remaining'],
        datasets: [
            {
                label: 'Budget',
                data: [budgetData.current_month_spent || 0, (budgetData.limit || 0) - (budgetData.current_month_spent || 0)],
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
            {popupMessage && <div style={{ color: 'red' }}>{popupMessage}</div>}
            <div>
                <label>
                    New Budget Limit:
                    <input type="number" value={newLimit} onChange={(e) => setNewLimit(e.target.value)} />
                    {errors.newLimit && <span style={{ color: 'red' }}>{errors.newLimit}</span>}
                </label>
                <button onClick={handleLimitChange}>Update Limit</button>
            </div>
            <div>
                <label>
                    Purchase Amount:
                    <input type="number" value={purchaseAmount} onChange={(e) => setPurchaseAmount(e.target.value)} />
                    {errors.purchaseAmount && <span style={{ color: 'red' }}>{errors.purchaseAmount}</span>}
                </label>
                <button onClick={handlePurchase}>Add Purchase</button>
            </div>
            <div>
                <label>
                    Month:
                    <input type="number" value={month} onChange={(e) => setMonth(e.target.value)} />
                    {errors.month && <span style={{ color: 'red' }}>{errors.month}</span>}
                </label>
                <label>
                    Year:
                    <input type="number" value={year} onChange={(e) => setYear(e.target.value)} />
                    {errors.year && <span style={{ color: 'red' }}>{errors.year}</span>}
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
