// Objet global pour stocker les taux de change par date
const ratesData = {};

// Fonction exécutée lorsque le DOM est entièrement chargé
document.addEventListener('DOMContentLoaded', function() {
    const reloadButton = document.getElementById('reload-btn');
    const dateInput = document.getElementById('date-picker');

    if (reloadButton && dateInput) {
        reloadButton.addEventListener('click', fetchRates);
        dateInput.addEventListener('change', fetchRates);
    }
});

// Fonction pour récupérer les taux de change depuis le serveur
async function fetchRates() {
    const date = document.getElementById('date-picker').value;
    const ratesTableBody = document.getElementById('rates-table-body');
    const dynamicPhrase = document.getElementById('dynamicPhrase');
    
    // Afficher le message de chargement et effacer la phrase dynamique
    ratesTableBody.innerHTML = '<tr><td colspan="5">Loading...</td></tr>';

    // Effacer la phrase dynamique au début, pour montrer le chargement en cours
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

        // Stocker les données dans l'objet global
        ratesData[date] = data.rates;
        displayRates();  // Afficher toutes les données stockées
        updateDynamicPhrase(date, data.rates); // Mettre à jour la phrase dynamique
    } catch (error) {
        console.error('Error fetching rates:', error);
        ratesTableBody.innerHTML = '<tr><td colspan="5">Error fetching rates.</td></tr>';
    }
}

// Fonction pour afficher les taux de change dans le tableau
function displayRates() {
    const ratesTableBody = document.getElementById('rates-table-body');

    // Effacer les lignes existantes
    ratesTableBody.innerHTML = '';

    // Parcourir toutes les dates et afficher les taux de change
    for (const [date, rates] of Object.entries(ratesData)) {
        const row = document.createElement('tr');
        
        // Créer la cellule de la date
        const dateCell = document.createElement('td');
        dateCell.textContent = date;
        row.appendChild(dateCell);

        // Définir les devises à afficher
        const currencies = ['EUR', 'USD', 'JPY', 'GBP'];

        let isValidRow = true;  // Drapeau pour déterminer si la ligne doit être ajoutée

        // Ajouter les cellules pour chaque devise
        currencies.forEach(currency => {
            const rateCell = document.createElement('td');
            if (rates[currency] === undefined || rates[currency] === null) {
                rateCell.textContent = 'N/A';
                isValidRow = false;  // Marquer la ligne comme invalide si une cellule contient 'N/A'
            } else {
                rateCell.textContent = rates[currency];
            }
            row.appendChild(rateCell);
        });

        // Ajouter la ligne au corps du tableau uniquement si elle est valide
        if (isValidRow) {
            ratesTableBody.appendChild(row);
        }
    }
}
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { day: 'numeric', month: 'long', year: 'numeric' };
    return date.toLocaleDateString('en-GB', options); // Format anglais
}



// Fonction pour mettre à jour la phrase dynamique
function updateDynamicPhrase(date, rates) {
    const dynamicPhrase = document.getElementById('dynamicPhrase');
    const formattedDate = formatDate(date);

    const eurRate = rates['EUR'] ?? 'loading';
    const usdRate = rates['USD'] ?? 'loading';
    const jpyRate = rates['JPY'] ?? 'loading';
    const gbpRate = rates['GBP'] ?? 'loading';

    // Mettre à jour la phrase dynamique
    dynamicPhrase.textContent = `Exchange rates for ${formattedDate} are: Euro = ${eurRate}, US Dollar = ${usdRate}, Japanese Yen = ${jpyRate}, British Pound = ${gbpRate}.`;

    // Effacer le message de chargement une fois que les données sont traitées
    const ratesTableBody = document.getElementById('rates-table-body');
    if (ratesTableBody.innerHTML.includes('Loading...')) {
        ratesTableBody.innerHTML = ''; // Clear the loading message
    }
}
