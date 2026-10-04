const loginForm = document.getElementById('login-form');
const loginButton = document.getElementById('login-button');
const employeeIdInput = document.getElementById('employee-id');
const passwordInput = document.getElementById('password');

loginForm.addEventListener('submit', function (event) {
    event.preventDefault();

    const employeeId = employeeIdInput.value.trim();
    const password = passwordInput.value;

    if (!employeeId || !password) {
        return;
    }

    loginButton.disabled = true;
    loginButton.innerHtml = '<i class="fas fa-spinner fa-spin"></i> Signing in...';
})