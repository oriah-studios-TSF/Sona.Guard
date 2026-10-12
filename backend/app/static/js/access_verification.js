/**
 * sona.guard - Resident Access Verification Controller
 *
 * Coordinates the guard verification workstation interface:
 * 1. Loads and populates active estate entrance points dynamically from the backend.
 * 2. Captures guard input for resident lookup and checkpoint selection.
 * 3. Communicates with Flask backend APIs (`/access/entrances` and `/access/resident/<code`).
 * 4. Renders resident identification, residential property context, entrance gate status,
 *    and authoritative access eligibility decisions.
 *
 * Security Boundary:
 * All access decisions (resident active status, property standing, entrance assignment)
 * are calculated and enforced strictly by the Flask backend (Python). This client script
 * purely presents the authoritative server verdict and reasons to the security guard.
 */

// DOM Elements: Form controls, feedback containers, and profile display sections
const personSearchForm = document.getElementById('search-person-form')
const residentCodeInput = document.getElementById('resident-code-input')
const SearchPersonButton = document.getElementById('search-person-button')
const searchMessage = document.getElementById('search-message')
const personDetails = document.getElementById('personal-details')
const serverError = document.getElementById('server-error')
const noResultsFound = document.getElementById('no-results-found')
const entranceSelect = document.getElementById('entrance-selector')
const verifyAccessButton = document.getElementById('verify-access-btn')
const verifiedResult = document.getElementById('verified-result')
const verificationResult = document.getElementById('verification-result')
const verificationLoader = document.getElementById('verification-loader')
const verificationMessage = document.getElementById('verification-message')
const verificationIcon = document.getElementById('verification-icon')

/**
 * Asynchronously fetches and populates the list of active estate entrances.
 *
 * Communicates with the Flask endpoint `GET /access/entrances`.
 * Disables the dropdown during loading to prevent interaction before data arrives,
 * creates DOM option elements dynamically, and defaults to 'Main Vehicle Gate' if available.
 *
 * @async
 * @returns {Promise<void>} Resolves once entrances are populated or a fallback error option is set.
 */
async function loadEntrances() {
    // Disable dropdown while fetching to prevent premature selection or race conditions
    entranceSelect.disabled = true;

    try {
        // Fetch active gate checkpoints from Flask access control blueprint
        const response = await fetch('/access/entrances');
        const data = await response.json();

        // Validate HTTP response status and API business success flag
        if (!response || !data.success) {
            throw new Error(data.message || 'Unable to load entrances');
        }

        // Clear existing placeholder options (e.g., 'Loading access points...')
        entranceSelect.replaceChildren();

        // Handle empty entrance list gracefully
        if (data.entrances.length === 0) {
            entranceSelect.add(new Option('No active entrances available', ''))
            return;
        }

        // Populate dropdown with active entrance gates (text: name, value: database ID)
        data.entrances.forEach(function (entrance) {
            const option = new Option(entrance.name, entrance.id)
            entranceSelect.add(option)
        });

        // Smart default: Select 'Main Vehicle Gate' as primary checkpoint if present
        const mainGate = data.entrances.find(function (entrance) {
            return entrance.name === 'Main Vehicle Gate';
        });

        if (mainGate) {
            entranceSelect.value = String(mainGate.id);
        } else {
            entranceSelect.selectIndex = 0;
        }

    } catch (error) {
        // Network or server parsing failure: log error and present fallback option
        console.error('Error fetching entrances:', error);
        entranceSelect.replaceChildren(
            new Option('Unable to load entrances', '')
        );
    } finally {
        // Guarantee the selector is re-enabled once loading finishes (success or failure)
        entranceSelect.disabled = false;
    }
}

// Bootstrap checkpoint options as soon as the script evaluates on page load
loadEntrances();

/**
 * Handles the resident verification form submission.
 *
 * Flow:
 * 1. Intercepts submission to prevent a browser page reload.
 * 2. Normalizes and validates resident input and entrance selection.
 * 3. Dispatches an async GET request to `/access/resident/<code` with the selected `entrance_id`.
 * 4. Unpacks and renders the multi-entity response (resident, property, entrance, eligibility).
 * 5. Handles API business failures (e.g., 404 Not Found) and network transport errors.
 */
personSearchForm.addEventListener('submit', async function (event) {
    // Prevent the default browser form submission (full page reload)
    event.preventDefault();

    // Normalize input: trim leading/trailing whitespace and uppercase to match standard code formats (e.g., 'SONA-RES-001')
    const residentCode = residentCodeInput.value.trim().toUpperCase();

    // Guard clause: Ensure a search query was provided before contacting the server
    if (!residentCode) {
        searchMessage.textContent = 'Please provide a resident identifier for verification.'
        return;
    }

    // Reset UI state: Hide previous results and error banners prior to new query
    personDetails.style.display = 'none';
    noResultsFound.style.display = 'none';
    serverError.style.display = 'none';
    verifiedResult.style.display = 'none';
    
    // Enter loading state: Disable button to prevent concurrent duplicate submissions and display spinner
    SearchPersonButton.disabled = true;
    searchMessage.innerHTML = '<i class="fas fa-spinner"></i> Validating access credentials...';

    // Guard clause: Ensure an entrance is selected.
    // The backend requires an entrance ID to evaluate gate-specific access rules.
    if (!entranceSelect.value) {
        searchMessage.textContent = 'Please select an entrance before retrieving resident details.';
        noResultsFound.style.display = 'flex';
        return;
    }

    try {
        // Query resident verification endpoint.
        // encodeURIComponent protects against special characters or malformed URI components.
        const response = await fetch(
            `/access/resident/${encodeURIComponent(residentCode)}?entrance_id=${encodeURIComponent(entranceSelect.value)}`
        );

        const data = await response.json();

        // Check for non-200 HTTP status or application-level failure (e.g. 404 Resident Not Found)
        if (!response.ok || !data.success) {
            searchMessage.textContent = data.message || 'Unable to locate resident information.';
            noResultsFound.style.display = 'flex';
            return;
        }

        // Unpack structured data entities returned by Flask serializer
        const resident = data.resident;

        // Set hidden form field for resident ID
        document.getElementById('resident-code').dataset.residentId = resident.id;
        
        const property = data.property;
        const entrance = data.entrance;
        const eligibility = data.eligibility;
        const lastAttempt = data.last_access_attempt;

        // Render Profile Header
        document.getElementById('profile-full-name').textContent = resident.full_name;
        document.getElementById('profile-resident-code').textContent = resident.resident_code;
        const profileStatus = document.getElementById('profile-status');
        
        profileStatus.innerHTML = resident.is_active ? '<i class="fa-solid fa-circle-check"></i> Active Resident' : '<i class="fa-solid fa-circle-xmark"></i> Inactive Resident';
        profileStatus.classList.add(resident.is_active ? 'active-profile-status' : 'inactive-profile-status');
        profileStatus.classList.remove(resident.is_active ? 'inactive-profile-status' : 'active-profile-status');

        // Render Resident Contact & Identification Information
        document.getElementById('resident-full-name').textContent = resident.full_name;
        document.getElementById('resident-code').textContent = resident.resident_code;
        document.getElementById('unit-number').textContent = resident.unit_number || 'N/A';
        document.getElementById('email-address').textContent = resident.email || 'N/A';
        document.getElementById('phone-number').textContent = resident.phone_number || 'N/A';

        // Render Residence / Property Information
        document.getElementById('estate-name').textContent = property.name;
        document.getElementById('estate-address').textContent = property.address;
        document.getElementById('resident-unit-number').textContent = resident.unit_number || 'N/A';
        document.getElementById('residence-address').textContent = property.address || 'N/A';

        // Render Access Authorization & Gate Eligibility Decision
        // Note: 'eligibility.reason' contains the authoritative access decision evaluated by the backend
        const accessStatus = document.getElementById('access-status');
        
        accessStatus.innerHTML = eligibility.is_eligible ? `<i class="fas fa-check-circle"></i> ${eligibility.reason}` : `<i class="fas fa-times-circle"></i> ${eligibility.reason}`;
        
        accessStatus.classList.remove('eligible', 'ineligible');
        accessStatus.classList.add(eligibility.is_eligible ? 'eligible' : 'ineligible');
        
        const propertyStatus = document.getElementById('property-status');

        propertyStatus.innerHTML = property.status ? '<i class="fas fa-check-circle"></i> Active' : '<i class="fas fa-times-circle"></i> Inactive';

        propertyStatus.classList.remove('eligible', 'ineligible');
        propertyStatus.classList.add(property.status ? 'eligible' : 'ineligible');

        const entranceStatus = document.getElementById('entrance-status');

        entranceStatus.innerHTML = entrance.status ? `<i class="fas fa-check-circle"></i> ${entrance.name} - ${entrance.status}` : `<i class="fas fa-times-circle"></i> ${entrance.name} - ${entrance.status}`;

        entranceStatus.classList.remove('eligible', 'ineligible');
        entranceStatus.classList.add(entrance.status ? 'eligible' : 'ineligible');
        
        document.getElementById('last-access-attempt').textContent = lastAttempt ? `${lastAttempt.result} - ${new Date(lastAttempt.created_at).toLocaleString('en-ZA', { timeZone: 'Africa/Johannesburg' }).replace(',', '')}` : 'No access attempts recorderd';
        
        // Display result card and clear status message
        personDetails.style.display = 'block';
        noResultsFound.style.display = 'none';
        searchMessage.textContent = '';
        
    } catch (error) {
        // Network transport failure (e.g., lost connection, DNS failure, server unreachable)
        console.log('Error fetching resident information: ', error);
        searchMessage.innerHTML = '<i class="fas fa-triangle-exclamation"></i> Unable to connect to the server. Please try again.';
        serverError.style.display = 'flex';
        
    } finally {
        // Guarantee button is re-enabled regardless of outcome so guard can retry or search again
        SearchPersonButton.disabled = false;
    }
});

verifyAccessButton.addEventListener('click', async function () {
    // Get the resident currently displayed on the verification page.
    const residentId = document.getElementById('resident-code').dataset.residentId;

    // Display loader while waiting for response. Hide person details.
    verificationLoader.style.display = 'flex';
    personDetails.style.display = 'none';

    // Get the entrance selected by the guard.
    const entranceId = entranceSelect.value;

    // Make sure a resident has been retrived first.
    if (!residentId) {
        alert('Please retrieve a resident before verifying access.')
        return;
    }

    // Make sure an entrance has been selected.
    if (!entranceId) {
        alert('Please select an entrance before verifying access.')
        return;
    }

    // Prevent duplicate requests while verification is in progress.
    verifyAccessButton.disabled = true;
    
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    try {
        // Send the resident and entrance IDs to Flask for verification.
        const response = await fetch('/access/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken  // Include the CSRF token in the headers.
            },
            body: JSON.stringify({
                resident_id: residentId,
                entrance_id: entranceId
            })
        });

        // Convert Flask's JSON response into a Javascript object.
        const data = await response.json();
        
        verificationLoader.style.display = 'none';

        // Display the decision returned by the backend.
        if (data.result === 'GRANTED') {
            // Remove the error class from the result container. Set a timout to hide the result after 6 seconds.
            verifiedResult.style.display = 'flex';
            verifiedResult.classList.add('verified-result-success');
            verificationIcon.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
            verificationResult.textContent = 'Access Granted'
            verificationMessage.textContent = `${data.reason} Resident may proceed to enter the premises.`;

            setTimeout(() => {
                verifiedResult.style.display = 'none';
            }, 6000);
        } else {
            // Add the error class to the result container. Set a timout to hide the result after 6 seconds.
            // This will make the result container red.
            verifiedResult.style.display = 'flex';
            verifiedResult.classList.add('verified-result-error');
            verificationIcon.innerHTML = '<i class="fa-solid fa-circle-xmark"></i>';
            verificationResult.textContent = 'Access Denied'
            verificationMessage.textContent = `${data.reason || data.message} Resident may not proceed to enter the premises.`;

            setTimeout(() => {
                verifiedResult.style.display = 'none';
            }, 6000);
        }

        console.log('Access verification result:', data);
        
    } catch (error) {
        // Handle network failures or unexpected server response
        console.error('Error verifying access:', error);
        
        // Display an error message to the user
        verifiedResult.ClassList.add('verified-result-error');
        verifiedResult.style.display = 'flex';
        verificationIcon.innerHTML = '<i class="fa-solid fa-xmark"></i>';
        verificationResult.textContent = 'Access Denied'
        verificationMessage.textContent = 'An error occurred while verifying access. Please try again later.';

        setTimeout(() => {
            verifiedResult.style.display = 'none';
        }, 6000);
    } finally {
        // Re-enable the button after verification is complete. For the guard to be able to verify again.
        verifyAccessButton.disabled = false;
    }
});