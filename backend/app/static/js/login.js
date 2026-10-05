const loginForm = document.getElementById('login-form');
const loginButton = document.getElementById('login-button');

const employeeIdInput = document.getElementById('employee-id');
const passwordInput = document.getElementById('password');

const employeeIdError = document.getElementById('employee-id-error');
const passwordError = document.getElementById('password-error');

const toast = document.getElementById('toast');

loginForm.addEventListener('submit', async function (event) {
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

    try {
        const response = await fetch('/auth/sign-in', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
            },
                
            body: JSON.stringify({
                employee_id: employeeId,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (!response.ok || !data.success) {
            toast.innerHTML = `<i class="fas fa-triangle-exclamation"></i> ${data.message}`;
            toast.classList.add('error');
            toast.style.display = 'block';

            loginButton.disabled = false;
            loginButton.innerHTML = '<i class="fas fa-sign-in-alt"></i> Sign In';

            return;
        }

        window.location.href = '/dashboard';
        
    } catch (error) {
        toast.innerHTML = `<i class="fas fa-triangle-exclamation"></i> Unable to connect to the server. Please try again.`;
        toast.classList.add('error');
        toast.style.display = 'block';

        loginButton.disabled = false;
        loginButton.innerHTML = '<i class="fas fa-sign-in-alt"></i> Sign In';
    }
});