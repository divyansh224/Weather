// Handle form submission
const loginForm = document.getElementById('loginForm');

loginForm.addEventListener('submit', (event) => {
    event.preventDefault();

    // Get form values
    const emailOrPhone = document.getElementById('emailOrPhone').value;
    const password = document.getElementById('password').value;

    // Here, you would typically send an AJAX request to your server to validate credentials
    // and perform the login process. For now, let's simulate a successful login:

    if (emailOrPhone === 'divyanshk337@gmail.com' && password === '1234') {
        // Redirect to the dashboard or another protected page
        sessionStorage.setItem('isAuthenticated','true')
        window.location.href = 'index.html';
    } else {
        // Display an error message (you can customize this)
        alert('Invalid email/phone or password.');
    }
});