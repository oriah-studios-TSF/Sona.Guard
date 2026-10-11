const loginForm = document.getElementById('login-form');
const loginButton = document.getElementById('login-button');

const staffCodeInput = document.getElementById('staff-code');
const passwordInput = document.getElementById('password');

const staffCodeError = document.getElementById('staff-code-error');
const passwordError = document.getElementById('password-error');

const toast = document.getElementById('toast');

const serverToastData = document.getElementById('server-toast-data');

function showToast(message, category = 'error') {
    let icon = 'fa-triangle-exclamation';

    if (category === 'success') {
        icon = 'fa-circle-check';
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

loginForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const staffCode = staffCodeInput.value.trim();
    const password = passwordInput.value;

    staffCodeError.innerHTML = '';
    staffCodeError.style.display = 'none';

    passwordError.innerHTML = '';
    passwordError.style.display = 'none';

    let isValid = true;

    if (!staffCode) {
        staffCodeError.innerHTML = '<i class="fas fa-triangle-exclamation"></i>  Staff code is required';
        staffCodeError.style.display = 'block';
        isValid = false;
    }

    if (!password) {
        passwordError.innerHTML = '<i class="fas fa-triangle-exclamation"></i> Password is required';
        passwordError.style.display = 'block';
        isValid = false;
    }

    if (!isValid) {
        return;
    }

    loginButton.disabled = true;
    loginButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Logging in...';

    try {
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
            },
                
            body: JSON.stringify({
                staff_code: staffCode,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (!response.ok || !data.success) {
            showToast(data.message, 'error');

            loginButton.disabled = false;
            loginButton.innerHTML = '<i class="fas fa-sign-in-alt"></i> Login';

            return;
        }

        window.location.href = '/dashboard/';
        
    } catch (error) {
        showToast('Unable to connect to the server. Please try again.', 'error');

        loginButton.disabled = false;
        loginButton.innerHTML = '<i class="fas fa-sign-in-alt"></i> Login';
    }
});