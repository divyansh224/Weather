// Handle form submission
const loginForm = document.getElementById('loginForm');

loginForm.addEventListener('submit', (event) => {
    event.preventDefault();

    // Get form values
    const emailOrPhone = document.getElementById('emailOrPhone').value;
    const password = document.getElementById('password').value;

    // Here, you would typically send an AJAX request to your server to validate credentials
    // and perform the login process. For now, let's simulate a successful login:

    if (emailOrPhone === 'your_email@example.com' && password === 'your_password') {
        // Redirect to the dashboard or another protected page
        window.location.href = 'dashboard.html';
    } else {
        // Display an error message (you can customize this)
        alert('Invalid email/phone or password.');
    }
});