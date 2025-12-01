document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Clear previous errors
    clearErrors();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    // Client-side validation
    let isValid = true;
    
    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showError('emailError', 'Please enter a valid email address');
        isValid = false;
    }
    
    // Password length validation
    if (password.length < 8) {
        showError('passwordError', 'Password must be at least 8 characters long');
        isValid = false;
    }
    
    // Confirm password validation
    if (password !== confirmPassword) {
        showError('confirmPasswordError', 'Passwords do not match');
        isValid = false;
    }
    
    if (!isValid) {
        return;
    }
    
    // Send registration request
    try {
        const response = await fetch('/register', {
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
            showMessage('Registration successful! Redirecting...', 'success');
            setTimeout(() => {
                window.location.href = '/login-page';
            }, 2000);
        } else {
            showMessage(data.detail || 'Registration failed', 'error');
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
