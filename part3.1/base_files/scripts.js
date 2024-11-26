document.addEventListener('DOMContentLoaded', () => {
    const isIndexPage = document.getElementById('places-list') !== null;
    const isDetailPage = document.getElementById('place-details') !== null;
    const isLoginPage = document.getElementById('login-form') !== null;

    const token = checkAuthentication();

    if (isIndexPage) {
        fetchPlaces();
        initializePriceFilter();
    } else if (isDetailPage) {
        const placeId = getPlaceIdFromURL();
        if (placeId) {
            fetchPlaceDetails(token, placeId);
        }
    } else if (isLoginPage) {
        initializeLoginForm();
    }
});

function initializeLoginForm() {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
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
                    document.cookie = `token=${data.access_token}; path=/`;
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
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
    return null; 
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
        if (addReviewSection) addReviewSection.style.display = 'none';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        if (addReviewSection) addReviewSection.style.display = 'block';
        console.log('User authenticated. Token:', token);
    }
    return token;
}

async function fetchPlaces() {
    try {
        const response = await fetch('http://127.0.0.1:5050/api/v1/places', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const places = await response.json();
            console.log('Places fetched successfully:', places);
            displayPlaces(places);
        } else {
            console.error('Failed to fetch places:', response.statusText);
            alert('Unable to fetch places. Please try again later.');
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        alert('An error occurred while fetching places.');
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) {
        console.error('Element #places-list not found - wrong page?');
        return;
    }
    placesList.innerHTML = '';

    places.forEach(place => {
        const placeCard = document.createElement('article');
        placeCard.classList.add('place-card');

        placeCard.innerHTML = `
            <h3>${place.title}</h3>
            <p>${place.description}</p>
            <p>Price: $${place.price} per night</p>
            <button class="details-button">View Details</button>
        `;

        const detailsButton = placeCard.querySelector('.details-button');
        detailsButton.addEventListener('click', () => {
            window.location.href = `place.html?id=${place.id}`;
        });

        placesList.appendChild(placeCard);
    });
}

function initializePriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            const placeCards = document.querySelectorAll('.place-card');

            placeCards.forEach(card => {
                const priceText = card.querySelector('p:nth-of-type(2)').textContent;
                const price = parseInt(priceText.replace(/[^0-9]/g, ''));

                if (selectedPrice === 'all') {
                    card.style.display = 'block';
                } else {
                    card.style.display = price <= parseInt(selectedPrice) ? 'block' : 'none';
                }
            });
        });
    }
}

function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    
    if (!placeId) {
        console.error('No place ID found in URL');
        return null;
    }
    
    return placeId;
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const response = await fetch(`http://127.0.0.1:5050/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const placeDetails = await response.json();
            console.log('Place details fetched successfully:', placeDetails);
            displayPlaceDetails(placeDetails);
        } else {
            console.error('Failed to fetch place details:', response.statusText);
            alert('Unable to fetch place details. Please try again later.');
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
        alert('An error occurred while fetching place details.');
    }
}

function displayPlaceDetails(place) {
    const placeDetailsSection = document.getElementById('place-details');
    if (!placeDetailsSection) {
        console.error('Place details section not found');
        return;
    }

    placeDetailsSection.innerHTML = '';
    const detailsContainer = document.createElement('div');
    detailsContainer.classList.add('place-details-container');

    detailsContainer.innerHTML = `
        <h2>${place.title}</h2>
        <div class="place-info">
            <p class="description">${place.description}</p>
            <p class="price">Price: $${place.price} per night</p>
        </div>
    `;

    if (place.amenities && place.amenities.length > 0) {
        const amenitiesSection = document.createElement('div');
        amenitiesSection.classList.add('amenities-section');
        amenitiesSection.innerHTML = `
            <h3>Amenities</h3>
            <ul>
                ${place.amenities.map(amenity => `<li>${amenity}</li>`).join('')}
            </ul>
        `;
        detailsContainer.appendChild(amenitiesSection);
    }

    if (place.reviews && place.reviews.length > 0) {
        const reviewsSection = document.createElement('div');
        reviewsSection.classList.add('reviews-section');
        reviewsSection.innerHTML = `
            <h3>Reviews</h3>
            ${place.reviews.map(review => `
                <div class="review">
                    <p class="review-user">User: ${review.user}</p>
                    <p class="review-text">${review.text}</p>
                </div>
            `).join('')}
        `;
        detailsContainer.appendChild(reviewsSection);
    }

    placeDetailsSection.appendChild(detailsContainer);
}


