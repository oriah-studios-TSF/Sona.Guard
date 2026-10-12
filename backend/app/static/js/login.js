/**
 * sona.guard - Staff Authentication Controller
 *
 * Coordinates the staff login interface:
 * 1. Performs instant client-side validation for credentials.
 * 2. Transmits authentication credentials to `POST /auth/login` alongside a CSRF token.
 * 3. Handles server response codes and redirects authenticated staff to `/dashboard/`.
 * 4. Displays contextual toast notifications for system notices or authentication errors.
 *
 * Security Boundary:
 * Client-side validation only verifies that inputs are non-empty for immediate UX feedback.
 * The Flask backend (`auth.py`) is solely responsible for verifying credential authenticity,
 * Argon2/bcrypt password hashes, role privileges, and active account status.
 */

// Form elements and submission triggers
const loginForm = document.getElementById('login-form');
const loginButton = document.getElementById('login-button');

// Input fields for staff credentials
const staffCodeInput = document.getElementById('staff-code');
const passwordInput = document.getElementById('password');

// Field-specific validation message placeholders
const staffCodeError = document.getElementById('staff-code-error');
const passwordError = document.getElementById('password-error');

// Toast notification element for system-wide banners
const toast = document.getElementById('toast');

// Hidden DOM anchor carrying messages flashed by Flask (e.g. after logout or session expiry)
const serverToastData = document.getElementById('server-toast-data');

/**
 * Displays a temporary toast notification banner with category-specific icons.
 *
 * @param {string} message - The text content to display to the user.
 * @param {('error'|'warning'|'info'|'success')} [category='error'] - Visual theme category determining the icon and CSS styles.
 */
function showToast(message, category = 'error') {
    let icon = 'fa-triangle-exclamation';

    if (category === 'success') {
        icon = 'fa-circle-check';
    } else if (category === 'info') {
        icon = 'fa-circle-info';
    }

    // Set FontAwesome icon and sanitized message text
    toast.innerHTML = `<i class="fas ${icon}"></i> ${message}`;

    // Apply baseline and category-specific styling
    toast.className = 'toast';
    toast.classList.add(category);
    toast.style.display = 'block';

    // Auto-dismiss the toast notification after 4 seconds
    toastTimeout = setTimeout(() => {
        toast.style.display = 'none';
    }, 4000);
}

// Automatically display any flash messages injected by Flask into the template data attributes on page load
if (serverToastData) {
    showToast(
        serverToastData.dataset.message,
        serverToastData.dataset.category
    );
}

/**
 * Handles the login form submission.
 *
 * Flow:
 * 1. Prevents standard HTTP form submission.
 * 2. Validates presence of credentials client-side.
 * 3. Enters loading state (disabling button and displaying spinner).
 * 4. Dispatches an async POST request to `/auth/login` with JSON payload and CSRF token.
 * 5. Handles failed authentication by displaying server error message in a toast.
 * 6. Redirects successfully authenticated staff to the `/dashboard/`.
 */
loginForm.addEventListener('submit', async function (event) {
    // Intercept default HTML form submission to handle authentication asynchronously
    event.preventDefault();

    // Extract input values (trim whitespace from staff code; preserve raw password characters)
    const staffCode = staffCodeInput.value.trim();
    const password = passwordInput.value;

    // Reset inline error indicators prior to re-validation
    staffCodeError.innerHTML = '';
    staffCodeError.style.display = 'none';

    passwordError.innerHTML = '';
    passwordError.style.display = 'none';

    let isValid = true;

    // Validate that staff identifier is provided
    if (!staffCode) {
        staffCodeError.innerHTML = '<i class="fas fa-triangle-exclamation"></i>  Staff code is required';
        staffCodeError.style.display = 'block';
        isValid = false;
    }

    // Validate that password is provided
    if (!password) {
        passwordError.innerHTML = '<i class="fas fa-triangle-exclamation"></i> Password is required';
        passwordError.style.display = 'block';
        isValid = false;
    }

    // Stop execution if client-side validation failed, avoiding unnecessary network traffic
    if (!isValid) {
        return;
    }

    // Set UI loading state: Disable button to prevent double-submissions and show spinner
    loginButton.disabled = true;
    loginButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Logging in...';

    try {
        // Dispatch credentials to Flask authentication route
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Flask-WTF requires the CSRF token to protect against Cross-Site Request Forgery
                'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
            },
                
            body: JSON.stringify({
                staff_code: staffCode,
                password: password
            })
        });
        
        const data = await response.json();
        
        // Handle failed authentication (e.g. 401 Unauthorized, invalid credentials, inactive staff account)
        if (!response.ok || !data.success) {
            showToast(data.message, 'error');

            // Restore login button to allow retry
            loginButton.disabled = false;
            loginButton.innerHTML = '<i class="fas fa-sign-in-alt"></i> Login';

            return;
        }

        // On successful authentication, redirect user to the application dashboard
        window.location.href = '/dashboard/';
        
    } catch (error) {
        // Handle network drops or server connectivity failures
        showToast('Unable to connect to the server. Please try again.', 'error');

        // Restore login button on error
        loginButton.disabled = false;
        loginButton.innerHTML = '<i class="fas fa-sign-in-alt"></i> Login';
    }
});