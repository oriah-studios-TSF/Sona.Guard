const toast = document.getElementById('toast');
const serverToastData = document.getElementById('server-toast-data');
const logoutButton = document.getElementById('logout-button');
const csrfToken = document.getElementById('csrf-token');

let toastTimeout;

function showToast(message, category = 'success') {
    clearTimeout(toastTimeout);
    
    let icon = 'fa-circle-check';

    if (category === 'error' || category === 'warning') {
        icon = 'fa-triangle-exclamation';
    } else if (category === 'info') {
        icon = 'fa-circle-info';
    }

    toast.innerHTML = `<i class="fas ${icon}"></i> ${message}`;

    toast.className = 'toast';
    toast.classList.add(category);
    toast.style.display = 'block';

    toastTimeout = setTimeout(() => {
        toast.style.display = 'none';
    }, 4000);
}

if (serverToastData) {
    showToast(
        serverToastData.dataset.message,
        serverToastData.dataset.category
    );
}

if (logoutButton) {
    logoutButton.addEventListener('click', async function () {
        logoutButton.disabled = true;

        try {
            const response = await fetch('/auth/logout', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken.value
                }
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                showToast(data.message || 'Unable to log out.', 'error');
                logoutButton.disabled = false;
                return;
            }

            window.location.href = '/';
            

        } catch (error) {
            showToast('Unable to connect to the server. Please try again.', 'error');
            logoutButton.disabled = false;
        }
    });
}

function updateDateTime() {
    const now = new Date();

    document.getElementById('current-date').textContent =
        now.toLocaleDateString('en-ZA', {
            weekday: 'long',
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        });

    document.getElementById('current-time').textContent =
        now.toLocaleTimeString('en-ZA', {
            hour: '2-digit',
            minute: '2-digit',
        });
}

updateDateTime();
setInterval(updateDateTime, 1000);