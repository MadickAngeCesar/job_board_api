# Job Board API

## Overview

This project is a job board API developed using Flask, SQLite, and Flask-RESTful. It provides endpoints for submitting job applications, tracking application statuses, and managing application data. The API is designed to handle file uploads, validate input, and support basic CRUD operations for job applications.

## Project Structure

```
application_service/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── utils.py
│   └── config.py
│
├── venv/
│
├── migrations/
│
├── tests/
│   ├── __init__.py
│   ├── test_routes.py
│   └── test_models.py
│
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/job_board_api.git
   cd job_board_api
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database:**
   ```bash
   flask db upgrade
   ```

## Running the Application
```bash
flask run
```

## API Endpoints

### Job Application Submission

- **URL**: `/api/job/apply`
- **Method**: `POST`
- **Description**: Submit a job application with a resume and cover letter.

### Application Status

- **URL**: `/api/application/status`
- **Method**: `GET`
- **Description**: Retrieve the status of a job application.

## Testing with Postman

To test the API endpoints, you can use Postman:

1. Import the Postman collection provided in the repository.
2. Set up the environment variables as needed.
3. Test the `POST /api/job/apply` and `GET /api/application/status` endpoints.

## Tasks

### Task 9: Set up Application Service Boilerplate
- Description: Create a new Flask application for the Application Service. Set up the project structure, including directories for models, routes, and utilities. Initialize a virtual environment and install necessary dependencies.
- Estimated time: 3 hours

### Task 10: Implement Job Application Submission
- Description: Create API endpoints for submitting job applications. Handle file uploads (e.g., resumes, cover letters). Implement input validation and database storage for applications.
- Estimated time: 6 hours

### Task 11: Develop Application Tracking and Status Management
- Description: Create API endpoints for retrieving and updating application statuses. Implement status change notifications (integrate with Notification Service).
- Estimated time: 5 hours