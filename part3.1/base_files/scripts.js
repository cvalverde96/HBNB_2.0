/* Event listener para login form */
document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            /* para recibir email y password del form */
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            /* request del API */
            try {
                const response = await fetch('http://127.0.0.1:5050/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password }) 
                });

                if (response.ok) {
                    const data = await response.json();
                    
                    /* guarda el JWT token en un cookie */
                    document.cookie = `token=${data.access_token}; path=/`;

                    /*redirect to index.html */
                    window.location.href = 'index.html';

                    console.log('Login successful:', data); 
                } else {
                    console.error('Login failed:', response.statusText);
                    alert('Invalid email or password. Please try again.');
                }
            } catch (error) {
                console.error('Error during login request:', error);
                alert('Something went wrong. Please try again later.');
            }
        });
    }
});

/* funcion para conseguir cooke por name */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null; 
}

/* funcion para validar si usuario esta autenticado */
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        console.log('User authenticated. Token:', token);
    }
}