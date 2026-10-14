/**
 * sona.guard - Administrative Layout Controller
 *
 * Provides shared global utilities across all authenticated guard/admin views:
 * 1. Global toast notification system with automatic dismissal timers.
 * 2. Automatic display of server-side flashed messages rendered in data attributes.
 * 3. Secure asynchronous user session termination (logout) with CSRF protection.
 * 4. Real-time security station clock formatted for the South African locale (`en-ZA`).
 */

// Global DOM elements for alerts and session controls
const toast = document.getElementById('toast');
const serverToastData = document.getElementById('server-toast-data');
const logoutButton = document.getElementById('logout-button');
const csrfToken = document.getElementById('csrf-token');
const loader = document.getElementById('loader');
const loaderMessage = document.getElementById('loader-message');

// Tracks active toast timer to prevent race conditions when multiple toasts fire sequentially
let toastTimeout;

/**
 * Displays an animated toast message banner with contextual iconography.
 *
 * If a previous toast is still visible, its dismissal timer is cancelled
 * to ensure the new message receives the full display duration.
 *
 * @param {string} message - Text notification to present to the user.
 * @param {('success'|'error'|'warning'|'info')} [category='success'] - Message classification affecting icon and palette.
 */
function showToast(message, category = 'success') {
    // Clear any existing dismissal timer to prevent early dismissal of the new message
    clearTimeout(toastTimeout);
    
    let icon = 'fa-circle-check';

    if (category === 'error' || category === 'warning') {
        icon = 'fa-triangle-exclamation';
    } else if (category === 'info') {
        icon = 'fa-circle-info';
    }

    // Set FontAwesome icon and message content
    toast.innerHTML = `<i class="fas ${icon}"></i> ${message}`;

    // Apply base class and category modifier
    toast.className = 'toast';
    toast.classList.add(category);
    toast.style.display = 'block';

    // Auto-hide notification after 4 seconds
    toastTimeout = setTimeout(() => {
        toast.style.display = 'none';
    }, 4000);
}

// Check for server-flashed messages (e.g., successful login or redirected notice) on initial page load
if (serverToastData) {
    showToast(
        serverToastData.dataset.message,
        serverToastData.dataset.category
    );
}

// Attach asynchronous logout event listener if the logout button exists in the DOM
if (logoutButton) {
    /**
     * Handles user logout asynchronously:
     * 1. Disables button to prevent multiple concurrent logout requests.
     * 2. Submits a POST request to `/auth/logout` with the required CSRF token.
     * 3. Redirects to the login page on success, or restores button state on error.
     */
    logoutButton.addEventListener('click', async function () {
        // Disable button immediately to prevent double-click race conditions
        logoutButton.disabled = true;
        loader.style.display = 'flex';
        loaderMessage.textContent = 'Logging out...';
        

        try {
            // Send logout request to Flask authentication blueprint
            const response = await fetch('/auth/logout', {
                method: 'POST',
                headers: {
                    // Include CSRF token header required by Flask-WTF for state-changing POST requests
                    'X-CSRFToken': csrfToken.value
                }
            });

            const data = await response.json();

            // Handle server-side logout rejection or failure
            if (!response.ok || !data.success) {
                showToast(data.message || 'Unable to log out.', 'error');
                logoutButton.disabled = false;
                return;
            }

            // Successfully logged out; redirect user to the login/landing page
            window.location.href = '/';
            

        } catch (error) {
            // Handle network transport failures (e.g., lost internet connection)
            showToast('Unable to connect to the server. Please try again.', 'error');
            logoutButton.disabled = false;
        }
    });
}

/**
 * Updates the security station header with the current date and time.
 * Formatted according to the South African locale standard (`en-ZA`).
 */
function updateDateTime() {
    const now = new Date();

    // Format full date: e.g. "Wednesday, 11 October 2026"
    document.getElementById('current-date').textContent =
        now.toLocaleDateString('en-ZA', {
            weekday: 'long',
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        });

    // Format 24-hour time: e.g. "22:07"
    document.getElementById('current-time').textContent =
        now.toLocaleTimeString('en-ZA', {
            hour: '2-digit',
            minute: '2-digit',
        });
}

// Initial invocation to render date and time immediately without a 1-second delay
updateDateTime();

// Keep the security station clock synchronized with a 1-second heartbeat
setInterval(updateDateTime, 1000);

// Everytime the page reloads display loader
window.addEventListener('beforeunload', function () {
    document.getElementById('loader').style.display = 'flex';
});