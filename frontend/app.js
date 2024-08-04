document.addEventListener('DOMContentLoaded', function() {
    // Ajouter des écouteurs d'événements pour le bouton et le sélecteur de date
    document.getElementById('reload-btn').addEventListener('click', fetchRates);
    document.getElementById('date-picker').addEventListener('change', fetchRates);
});

async function fetchRates() {
    const date = document.getElementById('date-picker').value;
    if (!date) {
        console.error('No date selected');
        return;
    }

    try {
        // Appel à la route pour récupérer les taux de change
        const response = await fetch(`http://127.0.0.1:5000/get_exchange_rates?date=${date}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        displayRates(data.rates);
    } catch (error) {
        console.error('Error fetching rates:', error);
        document.getElementById('rates-table-body').innerHTML = 'Error fetching rates.';
    }
}

function displayRates(rates) {
    const ratesTableBody = document.getElementById('rates-table-body');
    ratesTableBody.innerHTML = ''; // Clear previous results

    for (const [currency, rate] of Object.entries(rates)) {
        const row = document.createElement('tr');
        const currencyCell = document.createElement('td');
        currencyCell.textContent = currency;
        const rateCell = document.createElement('td');
        rateCell.textContent = rate;
        row.appendChild(currencyCell);
        row.appendChild(rateCell);
        ratesTableBody.appendChild(row);
    }
}