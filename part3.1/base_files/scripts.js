document.addEventListener('DOMContentLoaded', () => {
    const isIndexPage = document.getElementById('places-list') !== null;
    const isDetailPage = document.getElementById('place-details') !== null;
    const isLoginPage = document.getElementById('login-form') !== null;
    const isAddReviewPage = document.getElementById('review-form') !== null;

    if (isAddReviewPage) {
        initializeAddReview();
    }

    const token = checkAuthentication();

    if (!token && !isLoginPage) {
        window.location.href = 'login.html';
        return;
    }

    if (isIndexPage) {
        fetchPlaces();
        initializePriceFilter();
    } else if (isDetailPage && token) {
        const placeId = getPlaceIdFromURL();
        console.log(`Extracted placeId from URL: ${placeId}`);
        if (placeId) {
            fetchPlaceDetails(token, placeId);
            initializeReviewForm(token, placeId);
        }
    } else if (isLoginPage) {
        initializeLoginForm();
    }
});

// Utility functions
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
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
    }
    return token;
}

// Login
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
                } else {
                    throw new Error('Invalid email or password');
                }
            } catch (error) {
                console.error('Login error:', error);
                alert(error.message);
            }
        });
    }
}

// Places
async function fetchPlaces() {
    try {
        const response = await fetch('http://127.0.0.1:5050/api/v1/places');
        if (!response.ok) throw new Error('Failed to fetch places');
        const places = await response.json();
        displayPlaces(places);
    } catch (error) {
        console.error('Error:', error);
        alert(error.message);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    
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

// Price Filter
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

// Place Details and Reviews
function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const response = await fetch(`http://127.0.0.1:5050/api/v1/places/${placeId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) throw new Error('Failed to fetch place details');
        const placeDetails = await response.json();

        // Display place details
        displayPlaceDetails(placeDetails);

        // Fetch and display reviews for the place
        fetchReviews(placeId);
    } catch (error) {
        console.error('Error fetching place details:', error);
        alert('Unable to load place details at this time.');
    }
}

function displayPlaceDetails(place) {
    const placeDetailsSection = document.getElementById('place-details');
    if (!placeDetailsSection) return;

    placeDetailsSection.innerHTML = `
        <h2>${place.title}</h2>
        <div class="place-info">
            <p class="description">${place.description}</p>
            <p class="price">Price: $${place.price} per night</p>
        </div>
    `;

    if (place.amenities?.length) {
        const amenitiesSection = document.createElement('div');
        amenitiesSection.classList.add('amenities-section');
        amenitiesSection.innerHTML = `
            <h3>Amenities</h3>
            <ul>${place.amenities.map(amenity => `<li>${amenity}</li>`).join('')}</ul>
        `;
        placeDetailsSection.appendChild(amenitiesSection);
    }
}

async function fetchReviews(placeId) {
    console.log(`Fetching reviews for place_id: ${placeId}`);
    try {
        const response = await fetch(`http://127.0.0.1:5050/api/v1/places/${placeId}/reviews`);
        if (!response.ok) throw new Error('Failed to fetch reviews');
        const reviews = await response.json();
        console.log('Fetched reviews:', reviews);
        displayReviews(reviews);
    } catch (error) {
        console.error('Error fetching reviews:', error);
        alert('Unable to load reviews at this time.');
    }
}

function displayReviews(reviews) {
    const reviewsSection = document.getElementById('reviews');
    if (!reviewsSection) return;

    reviewsSection.innerHTML = '';

    if (reviews.length === 0) {
        reviewsSection.innerHTML = '<p>No reviews yet. Be the first to review!</p>';
    } else {
        reviews.forEach((review) => {
            const reviewCard = document.createElement('article');
            reviewCard.classList.add('review-card');
            reviewCard.innerHTML = `
                <h4>User: ${review.user_id}</h4>
                <p>Rating: ${review.rating}/5</p>
                <p>Comment: ${review.text}</p>
            `;
            reviewsSection.appendChild(reviewCard);
        });
    }
}

// Review Form
function initializeReviewForm(token, placeId) {
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const reviewText = document.getElementById('review').value;
            const rating = document.getElementById('rating').value;

            if (!reviewText || !rating) {
                alert('Please fill in all fields');
                return;
            }

            try {
                await submitReview(token, placeId, reviewText, rating);
                alert('Review submitted successfully!');
                window.location.href = `place.html?id=${placeId}`;
            } catch (error) {
                alert(error.message);
            }
        });
    }
}

async function submitReview(token, placeId, reviewText, rating) {
    try {
        const response = await fetch(`http://127.0.0.1:5050/api/v1/places/${placeId}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: parseInt(rating, 10)
            })
        });

        if (!response.ok) {
            throw new Error(`Failed to submit review: ${response.statusText}`);
        }

        console.log("Review submitted successfully.");
    } catch (error) {
        console.error("Error submitting review:", error);
        throw error;
    }
}

function initializeAddReview() {
    console.log("initializeAddReview called");
    
    // Check if the user is authenticated
    const token = checkAuthentication();
    if (!token) {
        console.log("User is not authenticated. Redirecting to login...");
        window.location.href = 'login.html';
        return;
    }

    // Extract the place ID from the URL
    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        console.error("No place ID found. Redirecting to index...");
        window.location.href = 'index.html';
        return;
    }

    // Handle review form submission
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const reviewText = document.getElementById('review-text').value;
            const rating = document.getElementById('rating').value;

            if (!reviewText || !rating) {
                alert("Please fill out all fields.");
                return;
            }

            try {
                // Submit the review
                await submitReview(token, placeId, reviewText, rating);
                alert("Review submitted successfully!");
                window.location.reload(); // Reload the page to see the new review
            } catch (error) {
                console.error("Error submitting review:", error);
                alert("Failed to submit review. Please try again.");
            }
        });
    } else {
        console.error("Review form not found in DOM.");
    }
}
