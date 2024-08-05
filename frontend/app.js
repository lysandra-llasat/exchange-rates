// Global object to store exchange rates by date
const ratesData = {};

// Function executed when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    const reloadButton = document.getElementById('reload-btn');
    const dateInput = document.getElementById('date-picker');

    if (reloadButton && dateInput) {
        reloadButton.addEventListener('click', fetchRates);
        dateInput.addEventListener('change', fetchRates);
    }
});

// Function to fetch exchange rates from the server
async function fetchRates() {
    const date = document.getElementById('date-picker').value;
    const ratesTableBody = document.getElementById('rates-table-body');
    const dynamicPhrase = document.getElementById('dynamicPhrase');

    // Show loading message and clear dynamic phrase
    ratesTableBody.innerHTML = '<tr><td colspan="5">Loading...</td></tr>';
    dynamicPhrase.textContent = '';

    if (!date) {
        ratesTableBody.innerHTML = '<tr><td colspan="5">Please select a date.</td></tr>';
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/get_exchange_rates?date=${date}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();

        // Store data in the global object
        ratesData[date] = data.rates;
        displayRates(); // Display all stored data
        updateDynamicPhrase(date, data.rates); // Update the dynamic phrase
    } catch (error) {
        console.error('Error fetching rates:', error);
        ratesTableBody.innerHTML = '<tr><td colspan="5">Error fetching rates.</td></tr>';
    }
}

// Function to display exchange rates in the table
function displayRates() {
    const ratesTableBody = document.getElementById('rates-table-body');

    // Clear existing rows
    ratesTableBody.innerHTML = '';

    // Loop through all dates and display exchange rates
    for (const [date, rates] of Object.entries(ratesData)) {
        const row = document.createElement('tr');
        
        // Create date cell
        const dateCell = document.createElement('td');
        dateCell.textContent = date;
        row.appendChild(dateCell);

        // Define currencies to display
        const currencies = ['EUR', 'USD', 'JPY', 'GBP'];

        let isValidRow = true; // Flag to determine if the row should be added

        // Add cells for each currency
        currencies.forEach(currency => {
            const rateCell = document.createElement('td');
            if (rates[currency] === undefined || rates[currency] === null) {
                rateCell.textContent = 'N/A';
                isValidRow = false; // Mark the row as invalid if any cell contains 'N/A'
            } else {
                rateCell.textContent = rates[currency];
            }
            row.appendChild(rateCell);
        });

        // Append the row to the table body only if it's valid
        if (isValidRow) {
            ratesTableBody.appendChild(row);
        }
    }
}

// Function to format date to a more readable form
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { day: 'numeric', month: 'long', year: 'numeric' };
    return date.toLocaleDateString('en-GB', options); // English format
}

// Function to update the dynamic phrase
function updateDynamicPhrase(date, rates) {
    const dynamicPhrase = document.getElementById('dynamicPhrase');
    const formattedDate = formatDate(date);

    const eurRate = rates['EUR'] ?? 'loading';
    const usdRate = rates['USD'] ?? 'loading';
    const jpyRate = rates['JPY'] ?? 'loading';
    const gbpRate = rates['GBP'] ?? 'loading';

    // Update the dynamic phrase
    dynamicPhrase.textContent = `Exchange rates for ${formattedDate} are: Euro = ${eurRate}, US Dollar = ${usdRate}, Japanese Yen = ${jpyRate}, British Pound = ${gbpRate}.`;

    // Clear the loading message once data is processed
    const ratesTableBody = document.getElementById('rates-table-body');
    if (ratesTableBody.innerHTML.includes('Loading...')) {
        ratesTableBody.innerHTML = ''; // Clear the loading message
    }
}
