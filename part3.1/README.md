
# **HBnB Application**

This is a RESTful API project for the **HolbertonBnB (HBnB)** application. The API allows users to manage various entities such as `users`, `places`, `reviews`, and `amenities`. It provides endpoints for creating, retrieving, updating, and deleting these entities, following common REST principles.

## **Table of Contents**
- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Modules Overview](#modules-overview)
  - [app.py](#app.py)
  - [models](#models)
    - [BaseModel](#basemodel)
    - [User](#user)
    - [Place](#place)
    - [Review](#review)
    - [Amenity](#amenity)
  - [api](#api)
    - [Users API](#users-api)
    - [Places API](#places-api)
    - [Reviews API](#reviews-api)
    - [Amenities API](#amenities-api)
  - [persistence](#persistence)
    - [InMemoryRepository](#inmemoryrepository)
  - [services](#services)
    - [HBnBFacade](#hbnbfacade)
- [Testing](#testing)
- [API Endpoints](#api-endpoints)

## **Project Overview**

The **HBnB** project is a web-based platform allowing users to register, create places (such as apartments or houses for rent), post reviews, and associate amenities with places. The platform employs REST principles to offer an efficient and consistent API for managing data. This repository contains the API code written in Python using Flask-RESTx, as well as in-memory persistence.

## **Project Structure**

```
├── app
│   ├── api
│   │   ├── v1
│   │   │   ├── users.py
│   │   │   ├── places.py
│   │   │   ├── reviews.py
│   │   │   └── amenities.py
│   ├── models
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── persistence
│   │   └── repository.py
│   ├── services
│   │   └── facade.py
├── run.py
└── README.md
```

## **Installation**

To set up the project, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/hbnb.git
   cd hbnb
   ```

2. **Install the required dependencies**:
   Ensure you have `python3.10+` installed along with `Flask` and `Flask-RESTx`. Install dependencies using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   Start the API by running:
   ```bash
   python3 run.py
   ```

## **Usage**

After installation, the API will be running at `http://127.0.0.1:5000/`. You can use tools like `Postman` or `curl` to interact with the endpoints and perform operations on users, places, reviews, and amenities.

---

## **Modules Overview**

### **app.py**

This file is the entry point to the Flask application. It initializes the app and sets up the namespaces for the API routes.

### **models**

This directory contains the class definitions for the main objects (User, Place, Review, Amenity). All models inherit from `BaseModel`.

#### **BaseModel**

`BaseModel` provides common functionality across all models, including the automatic generation of unique IDs and the management of timestamps (`created_at` and `updated_at`). It contains methods for updating and string representation.

#### **User**

The `User` class represents a user of the system. It includes the following attributes:
- `first_name`: Required string (max 50 characters).
- `last_name`: Required string (max 50 characters).
- `email`: Unique and valid email address.
- `is_admin`: Boolean indicating admin status (default is `False`).

#### **Place**

The `Place` class represents a property that can be rented. Attributes include:
- `title`: String representing the place's title.
- `description`: Optional text describing the place.
- `price`: Positive float for the price.
- `latitude` and `longitude`: Float values for the location of the place.
- `owner`: A `User` instance representing the owner.
- `reviews`: A list of `Review` objects.
- `amenities`: A list of `Amenity` objects.

#### **Review**

The `Review` class represents a review left by a user on a place. Attributes include:
- `text`: The content of the review.
- `rating`: Integer rating (1-5).
- `place`: Reference to the `Place` being reviewed.
- `user`: Reference to the `User` who wrote the review.

#### **Amenity**

The `Amenity` class represents a feature or amenity available at a place. Attributes:
- `name`: A string (max 50 characters) representing the amenity name (e.g., "Wi-Fi", "Parking").

### **api**

This directory contains the API routes for each entity (`users`, `places`, `reviews`, `amenities`), all defined using Flask-RESTx. Each route maps HTTP methods to functions within the `HBnBFacade` service.

#### **Users API**

- **POST /api/v1/users/**: Create a new user.
- **GET /api/v1/users/{user_id}**: Retrieve user by ID.
- **GET /api/v1/users/**: Retrieve all users.
- **PUT /api/v1/users/{user_id}**: Update user details.

#### **Places API**

- **POST /api/v1/places/**: Create a new place.
- **GET /api/v1/places/**: Retrieve all places.
- **GET /api/v1/places/{place_id}**: Retrieve place details.
- **PUT /api/v1/places/{place_id}**: Update place information.

#### **Reviews API**

- **POST /api/v1/reviews/**: Create a new review.
- **GET /api/v1/reviews/**: Retrieve all reviews.
- **GET /api/v1/reviews/{review_id}**: Retrieve review by ID.
- **PUT /api/v1/reviews/{review_id}**: Update review.
- **DELETE /api/v1/reviews/{review_id}**: Delete a review.

#### **Amenities API**

- **POST /api/v1/amenities/**: Create a new amenity.
- **GET /api/v1/amenities/**: Retrieve all amenities.
- **GET /api/v1/amenities/{amenity_id}**: Retrieve amenity details.

### **persistence**

This directory contains the repository class for managing data storage.

#### **InMemoryRepository**

A simple in-memory repository that simulates a database. It stores data in Python dictionaries and provides CRUD operations.

### **services**

This directory contains the service layer, which integrates the models with the repository and business logic.

#### **HBnBFacade**

`HBnBFacade` provides methods to manage all the main entities (User, Place, Review, and Amenity). It acts as the middle layer between the API routes and the underlying data models.

---

## **Testing**

You can test the API using `curl` or tools like Postman. For example, to create a new user:
```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'
```

## **API Endpoints**

| Method | Endpoint                    | Description                |
|--------|-----------------------------|----------------------------|
| GET    | /api/v1/users/               | Retrieve all users         |
| POST   | /api/v1/users/               | Create a new user          |
| GET    | /api/v1/users/{user_id}      | Retrieve user by ID        |
| PUT    | /api/v1/users/{user_id}      | Update user by ID          |
| GET    | /api/v1/places/              | Retrieve all places        |
| POST   | /api/v1/places/              | Create a new place         |
| GET    | /api/v1/places/{place_id}    | Retrieve place by ID       |
| PUT    | /api/v1/places/{place_id}    | Update place by ID         |
| GET    | /api/v1/reviews/             | Retrieve all reviews       |
| POST   | /api/v1/reviews/             | Create a new review        |
| GET    | /api/v1/reviews/{review_id}  | Retrieve review by ID      |
| PUT    | /api/v1/reviews/{review_id}  | Update review by ID        |
| DELETE | /api/v1/reviews/{review_id}  | Delete a review
