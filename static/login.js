document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Clear previous errors
    clearErrors();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Basic client-side validation
    let isValid = true;
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showError('emailError', 'Please enter a valid email address');
        isValid = false;
    }
    
    if (password.length === 0) {
        showError('passwordError', 'Password is required');
        isValid = false;
    }
    
    if (!isValid) {
        return;
    }
    
    // Send login request
    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Store token
            localStorage.setItem('token', data.access_token);
            showMessage('Login successful!', 'success');
            setTimeout(() => {
                window.location.href = '/';
            }, 1500);
        } else {
            showMessage(data.detail || 'Login failed', 'error');
        }
    } catch (error) {
        showMessage('An error occurred. Please try again.', 'error');
    }
});

function showError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    errorElement.textContent = message;
    const inputElement = errorElement.previousElementSibling;
    inputElement.classList.add('invalid');
}

function clearErrors() {
    const errors = document.querySelectorAll('.error');
    errors.forEach(error => error.textContent = '');
    
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => input.classList.remove('invalid'));
}

function showMessage(message, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = message;
    messageDiv.className = `message ${type}`;
}
