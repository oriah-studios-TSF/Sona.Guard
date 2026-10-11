const personSearchForm = document.getElementById('search-person-form')
const residentCodeInput = document.getElementById('resident-code-input')
const SearchPersonButton = document.getElementById('search-person-button')
const searchMessage = document.getElementById('search-message')
const personDetails = document.getElementById('personal-details')
const serverError = document.getElementById('server-error')
const noResultsFound = document.getElementById('no-results-found')
const entranceSelect = document.getElementById('entrance-selector')

async function loadEntrances() {

    entranceSelect.disabled = true;

    try {
        const response = await fetch('/access/entrances');
        const data = await response.json();

        if (!response || !data.success) {
            throw new Error(data.message || 'Unable to load entrances');
        }

        entranceSelect.replaceChildren();

        if (data.entrances.length === 0) {
            entranceSelect.add(new Option('No active entrances available', ''))
            return;
        }

        data.entrances.forEach(function (entrance) {
            const option = new Option(entrance.name, entrance.id)
            entranceSelect.add(option)
        });

        const mainGate = data.entrances.find(function (entrance) {
            return entrance.name === 'Main Vehicle Gate';
        });

        if (mainGate) {
            entranceSelect.value = String(mainGate.id);
        } else {
            entranceSelect.selectIndex = 0;
        }

    } catch (error) {
        console.error('Error fetching entrances:', error);
        entranceSelect.replaceChildren(
            new Option('Unable to load entrances', '')
        );
    } finally {
        entranceSelect.disabled = false;
    }
}

loadEntrances();

personSearchForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const residentCode = residentCodeInput.value.trim().toUpperCase();

    if (!residentCode) {
        searchMessage.textContent = 'Please provide a resident identifier for verification.'
        return;
    }

    personDetails.style.display = 'none';
    noResultsFound.style.display = 'none';
    serverError.style.display = 'none';
    
    SearchPersonButton.disabled = true;
    searchMessage.innerHTML = '<i class="fas fa-spinner"></i> Validating access credentials...';

    console.log('Selected entrance:', entranceSelect.value);
    console.log('Selected entrance element:', entranceSelect);

    if (!entranceSelect.value) {
        searchMessage.textContent = 'Please select an entrance. Please select an entrance before retrieving resident details.';
        noResultsFound.style.display = 'flex';
        return;
    }

    try {
        const response = await fetch(
            `/access/resident/${encodeURIComponent(residentCode)}?entrance_id=${encodeURIComponent(entranceSelect.value)}`
        );

        const data = await response.json();

        if (!response.ok || !data.success) {
            searchMessage.textContent = data.message || 'Unable to locate resident information.';
            noResultsFound.style.display = 'flex';
            return;
        }

        const resident = data.resident;
        const property = data.property;
        const entrance = data.entrance;
        const eligibility = data.eligibility;
        const lastAttempt = data.last_access_attempt;

        // Profile Header
        document.getElementById('profile-full-name').textContent = resident.full_name;
        document.getElementById('profile-resident-code').textContent = resident.resident_code;
        document.getElementById('profile-status').textContent = resident.status ? 'Active Resident' : 'Inactive Resident';

        // Resident Information
        document.getElementById('resident-full-name').textContent = resident.full_name;
        document.getElementById('resident-code').textContent = resident.resident_code;
        document.getElementById('unit-number').textContent = resident.unit_number || 'N/A';
        document.getElementById('email-address').textContent = resident.email || 'N/A';
        document.getElementById('phone-number').textContent = resident.phone_number || 'N/A';

        // Resident Information
        document.getElementById('estate-name').textContent = property.name;
        document.getElementById('estate-address').textContent = property.address;
        document.getElementById('resident-unit-number').textContent = resident.unit_number || 'N/A';
        document.getElementById('residence-address').textContent = property.address || 'N/A';

        // Access status
        document.getElementById('access-status').textContent = eligibility.reason;
        document.getElementById('property-status').textContent = property.status;
        document.getElementById('entrance-status').textContent = `${entrance.name} - ${entrance.status}`;
        document.getElementById('last-access-attempt').textContent = lastAttempt ? `${lastAttempt.result} - ${new Date(lastAttempt.created_at).toLocaleString('en-ZA', { timeZone: 'Africa/Johannesburg' }).replace(',', '')}` : 'No access attempts recorderd';
        

        personDetails.style.display = 'block';
        noResultsFound.style.display = 'none';
        searchMessage.textContent = '';
        
    } catch (error) {
        console.log('Error fetching resident information: ', error);
        searchMessage.innerHTML = '<i class="fas fa-triangle-exclamation"></i> Unable to connect to the server. Please try again.';
        serverError.style.display = 'flex';
        
    } finally {
        SearchPersonButton.disabled = false;
    }
});