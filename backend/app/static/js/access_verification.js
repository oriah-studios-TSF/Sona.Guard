const personSearchForm = document.getElementById('search-person-form')
const residentCodeInput = document.getElementById('resident-code-input')
const SearchPersonButton = document.getElementById('search-person-button')
const searchMessage = document.getElementById('search-message')
const personDetails = document.getElementById('personal-details')
const serverError = document.getElementById('server-error')
const noResultsFound = document.getElementById('no-results-found')


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

    try {
        const response = await fetch(
            `/access/resident/${encodeURIComponent(residentCode)}`
        );

        const data = await response.json();

        if (!response.ok || !data.success) {
            searchMessage.textContent = data.message || 'Unable to locate resident information.';
            noResultsFound.style.display = 'flex';
            return;
        }

        const resident = data.resident;
        
        document.getElementById('profile-full-name').textContent = resident.full_name;
        document.getElementById('profile-resident-code').textContent = resident.resident_code;
        document.getElementById('profile-status').textContent = resident.status ? 'Active Resident' : 'Inactive Resident';

        document.getElementById('resident-full-name').textContent = resident.full_name;
        document.getElementById('resident-code').textContent = resident.resident_code;
        document.getElementById('unit-number').textContent = resident.unit_number || 'N/A';
        document.getElementById('email-address').textContent = resident.email || 'N/A';
        document.getElementById('phone-number').textContent = resident.phone_number || 'N/A';
        

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