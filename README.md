# Health and Fitness Tracker API

## Project Overview
This is a Django-based RESTful API for tracking health and fitness activities. It allows users to:
- Log physical activities (e.g., running, walking) and track their details (e.g., duration, distance, calories burned).
- Create and manage workout plans.
- Maintain a diet log to track food items and calories consumed.

The API uses token-based authentication to secure endpoints and ensure only authenticated users can access their data.

## Key Features
- **Activity Logging**: Track user activities including type, duration, distance, and calories burned.
- **Workout Plans**: Create, update, and delete personalized workout plans.
- **Diet Log**: Record food items and track calories.
- **User Authentication**: Secure access to the API using token-based authentication.
- **Data Validation**: Ensures valid data is entered for all activities, workout plans, and diet logs.

## Technologies Used
- **Django**: For building the backend of the application.
- **Django REST Framework**: To build the API endpoints.
- **SQLite**: Default database for storing data.
- **Token Authentication**: Provided by Django REST Framework for user authentication.

## API Endpoints
Below is a list of available endpoints:

### 1. Activity API
| Method | Endpoint               | Description                                  |
|--------|------------------------|----------------------------------------------|
| GET    | `/api/activities/`      | List all activities (authenticated users only). |
| POST   | `/api/activities/`      | Create a new activity.                       |
| PUT    | `/api/activities/{id}/` | Update an existing activity.                 |
| DELETE | `/api/activities/{id}/` | Delete an activity.                          |

### 2. Workout Plan API
| Method | Endpoint                   | Description                                  |
|--------|----------------------------|----------------------------------------------|
| GET    | `/api/workout-plans/`       | List all workout plans (authenticated users only). |
| POST   | `/api/workout-plans/`       | Create a new workout plan.                   |
| PUT    | `/api/workout-plans/{id}/`  | Update an existing workout plan.             |
| DELETE | `/api/workout-plans/{id}/`  | Delete a workout plan.                       |

### 3. Diet Log API
| Method | Endpoint                | Description                                  |
|--------|-------------------------|----------------------------------------------|
| GET    | `/api/diet-logs/`        | List all diet logs (authenticated users only). |
| POST   | `/api/diet-logs/`        | Create a new diet log entry.                 |
| PUT    | `/api/diet-logs/{id}/`   | Update an existing diet log.                 |
| DELETE | `/api/diet-logs/{id}/`   | Delete a diet log.                           |

## Installation and Setup

### Prerequisites
- Python 3.12
- Django 5.0
- Django REST Framework
- SQLite (default database)
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/NKHUBALALE/fitness_tracker_api.git
   cd fitness_tracker_api
   ```
2 **Create and activate a virtual environment:**
   
   **Windows**:

        
        venv\Scripts\activate 
         

**Linux/Mac**:

        python3 -m venv venv
        source venv/bin/activate

       
3. **Install the required dependencies**:
    ```bash 
    pip install -r requirements.txt

4. **Apply migrations to set up the database:**
5.**Create a superuser to access the Django admin panel(optional, but recommended for managing the admin panel):**
6.**Run the development server:**

#### You can now access the API at `http://127.0.0.1:8000/api/`.

### Testing the API with Postman

1.**Register a New User:**
    -Endpoint: /api/login/
    -Method: POST
    -Body:`{
    "username": "testuser",
    "password": "testpassword"
    "email": "test@example.com"
}`
2.**login**
    -Endpoint: /api/login/
    -Method: POST
    -Body:{
            "username": "testuser",
            "password": "testpassword"
}`
3.**login**
    -Endpoint: /api/login/
    -Method: POST
    -Body:`{
            "activity_type": "Running",
            "duration": 30,
            "distance": 5.0,
            "calories_burned": 300
            }
            `
4. **Retrieve Activities:**
    -Endpoint: /api/activities/
    -Method: GET
    -Headers: Authorization: Token your_token_here