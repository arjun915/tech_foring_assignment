# tech_foring_assignment
# Project Name

## Overview

This is a Django-based API project for managing **projects**, **tasks**, and **comments**. It provides endpoints to create, retrieve, update, and delete projects, tasks, and comments, along with JWT-based authentication for secure access.

---

## Setup Instructions

### 1. Clone the repository

Clone the repository to your local machine:

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Set up a virtual environment

To keep your project dependencies isolated, create a virtual environment and activate it.

#### For Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### For Windows:
```bash
python -m venv venv
.env\Scriptsctivate
```

### 3. Install dependencies

Install all the required dependencies:

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

Apply database migrations to set up the necessary tables:

```bash
python manage.py migrate
```

### 5. Create a superuser

Create a superuser to access the Django admin interface:

```bash
python manage.py createsuperuser
```

Follow the prompts to create the user.

### 6. Run the development server

Start the server:

```bash
python manage.py runserver
```

The server will be accessible at `http://127.0.0.1:8000/`.

---

## API Documentation

### Authentication

To interact with the API, you need to authenticate using a **JWT token**.

#### Obtain JWT token (Login)

- **Endpoint**: `POST /api/auth/login/`
- **Request Payload**:
  ```json
  {
    "username": "your-username",
    "password": "your-password"
  }
  ```

- **Response**:
  ```json
  {
    "token": "your-jwt-token"
  }
  ```

Include the token in the **Authorization** header for subsequent requests:

```bash
Authorization: Bearer <your-jwt-token>
```

### Endpoints

#### Projects
#### Before Retriving Create the Data
- **List Projects**: `GET /api/projects/`
  - Retrieves a list of all projects.
  
- **Create Project**: `POST /api/projects/`
  - Creates a new project.
  
- **Retrieve Project**: `GET /api/projects/{id}/`
  - Retrieves details of a specific project.
  
- **Update Project**: `PUT /api/projects/{id}/`
  - Updates an existing project.
  
- **Delete Project**: `DELETE /api/projects/{id}/`
  - Deletes a specific project.

#### Tasks

- **List Tasks**: `GET /api/projects/{project_id}/tasks/`
  - Retrieves a list of tasks within a project.
  
- **Create Task**: `POST /api/projects/{project_id}/tasks/`
  - Creates a new task within a project.
  
- **Retrieve Task**: `GET /api/tasks/{id}/`
  - Retrieves details of a specific task.
  
- **Update Task**: `PUT /api/tasks/{id}/`
  - Updates an existing task.
  
- **Delete Task**: `DELETE /api/tasks/{id}/`
  - Deletes a specific task.

#### Comments

- **List Comments**: `GET /api/tasks/{task_id}/comments/`
  - Retrieves all comments for a task.
  
- **Create Comment**: `POST /api/tasks/{task_id}/comments/`
  - Adds a comment to a task.
  
- **Retrieve Comment**: `GET /api/comments/{id}/`
  - Retrieves details of a specific comment.
  
- **Update Comment**: `PUT /api/comments/{id}/`
  - Updates an existing comment.
  
- **Delete Comment**: `DELETE /api/comments/{id}/`
  - Deletes a specific comment.

---

## Postman Collection

You can import the **Postman** collection to test all the available endpoints. Here's how to import the collection:

1. Open **Postman**.
2. Click on **Import** (the button on the top-left of the Postman interface).
3. Select **Import from Link** or **Upload Files**, depending on the method you're using.
4. Select the `Postman Collection` file in the repository or the link provided.

Once the collection is imported, you can start testing all API endpoints.

### Authentication in Postman

1. Make a **POST** request to `/api/auth/login/` with your username and password to obtain the JWT token.
2. Copy the token from the response.
3. For every other API request, add the token in the **Authorization** header as `Bearer <your-jwt-token>`.

---

---

## Troubleshooting

If you encounter any issues, make sure to check the following:
- Ensure that you have applied all the migrations.
- Check if your JWT token is correctly set in the **Authorization** header.
- Ensure your database is properly configured and running.

For any other issues, feel free to raise an issue in the GitHub repository.

---


