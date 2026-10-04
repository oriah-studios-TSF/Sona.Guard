const loginForm = document.getElementById('login-form');
const loginButton = document.getElementById('login-button');

const employeeIdInput = document.getElementById('employee-id');
const passwordInput = document.getElementById('password');

const employeeIdError = document.getElementById('employee-id-error');
const passwordError = document.getElementById('password-error');

loginForm.addEventListener('submit', function (event) {
    event.preventDefault();

    const employeeId = employeeIdInput.value.trim();
    const password = passwordInput.value;

    employeeIdError.innerHTML = '';
    employeeIdError.style.display = 'none';

    passwordError.innerHTML = '';
    passwordError.style.display = 'none';

    let isValid = true;

    if (!employeeId) {
        employeeIdError.innerHTML = '<i class="fas fa-triangle-exclamation"></i>  Employee ID is required';
        employeeIdError.style.display = 'block';
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
    loginButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Signing in...';
});