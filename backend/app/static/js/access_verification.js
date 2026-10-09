const personSearchForm = document.getElementById('search-person-form')
const employeeIdInput = document.getElementById('employee-id')
const SearchPersonButton = document.getElementById('search-person-button')
const searchMessage = document.getElementById('search-message')
const personDetails = document.getElementById('personal-details')

personSearchForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const employeeId = employeeIdInput.value.trim().toUpperCase();

    if (!employeeId) {
        searchMessage.textContent = 'Please enter an employee ID.'
        return;
    }

    personDetails.style.display = 'none';
    SearchPersonButton.disabled = true;
    searchMessage.innerHTML = '<i class="fas fa-spinner"></i> Validating access credentials...';

    try {
        const response = await fetch(
            `/access/person/${encodeURIComponent(employeeId)}`
        );

        const data = await response.json();

        if (!response.ok || !data.success) {
            searchMessage.textContent = data.message || 'Employee lookup failed.';
            return;
        }

        const person = data.person;

        document.getElementById('person-name').textContent = person.full_name;
        document.getElementById('person-role').textContent = person.role || 'Not Provided';
        document.getElementById('person-job-title').textContent = person.job_title || 'Not Provided';
        document.getElementById('person-employee-id').textContent = person.employee_id;
        document.getElementById('person-email').textContent = person.email || 'Not Provided';
        document.getElementById('person-phone').textContent = person.phone_number || 'Not Provided';
        document.getElementById('person-nationality').textContent = person.nationality || 'Not Provided'
        document.getElementById('person-department-allocated').textContent = person.department_allocated || 'Not Provided';
        document.getElementById('person-department').textContent = person.department || 'Not Provided';
        document.getElementById('person-access-level').textContent = person.access_level || 'Not Provided';
        document.getElementById('person-access-expiry-date').textContent = person.access_expiry_date || 'Not Provided';
        document.getElementById('person-location').textContent = person.location || 'Not Provided';
        document.getElementById('person-last-verified').textContent = person.last_verified || 'Not Provided';
        document.getElementById('person-status').textContent = person.is_active ? 'Active' : 'Inactive';

        searchMessage.innerHTML = '<i class="fas fa-circle-check"></i> Employee found successfully.';
        personDetails.style.display = 'block';
        
    } catch (error) {
        searchMessage.textContent = 'Unable to connect to the server. Please try again.';
    } finally {
        SearchPersonButton.disabled = false;
    }
});