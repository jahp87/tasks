
# FastAPI Task Management API with IP, Country, and Weather Logging

This FastAPI project provides a simple task management API that logs each request's IP address, country, and weather conditions. The project uses PostgreSQL as the database and integrates with free APIs to obtain weather and geolocation data.

## Features

- **OAuth2 Authentication**: Implement OAuth2 for secure API access.
- **Task Management**: Basic CRUD operations for managing tasks.
- **IP, Country, and Weather Logging**: Log IP address, country, and weather for every request.
- **PostgreSQL**: All data is stored in a PostgreSQL database.
- **Docker Support**: Use Docker for easy local testing and development.
- **FastAPI Documentation**: Built-in API docs at `/docs` or `/redoc`.

---

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [IP, Country, and Weather Logging](#ip-country-and-weather-logging)
- [Running with Docker](#running-with-docker)
- [Postman Collection](#postman-collection)
- [Environment Variables](#environment-variables)
- [License](#license)

---

## Installation

### Prerequisites

- Python 3.7+
- PostgreSQL
- Docker (optional for Docker setup)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/fastapi-task-api.git
   cd fastapi-task-api
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables by creating a `.env` file:

   ```
   DATABASE_URL=postgresql://username:password@localhost/dbname
   WEATHERAPI_KEY=your_weatherapi_key
   SECRET_KEY=your_secret_key
   ```

5. Apply database migrations:

   ```bash
   alembic upgrade head
   ```

6. Run the FastAPI application:

   ```bash
   uvicorn main:app --reload
   ```

---

## Configuration

### Database Configuration

This project uses PostgreSQL as the database engine. Set the database URL in the `.env` file as follows:

```
DATABASE_URL=postgresql://username:password@localhost/dbname
```

### WeatherAPI Configuration

Sign up at [WeatherAPI](https://www.weatherapi.com/) and get an API key. Add it to the `.env` file:

```
WEATHERAPI_KEY=your_weatherapi_key
```

---

## API Endpoints

Here’s a list of available API endpoints. Detailed Swagger documentation is available at `/docs` or `/redoc` after running the project.

| Method | Endpoint                | Description               | Auth Required |
|--------|-------------------------|---------------------------|---------------|
| POST   | `/tasks`                | Create a new task          | Yes           |
| GET    | `/tasks`                | Get all tasks              | Yes           |
| GET    | `/tasks/{task_id}`       | Get a specific task by ID  | Yes           |
| PUT    | `/tasks/{task_id}`       | Update a specific task     | Yes           |
| DELETE | `/tasks/{task_id}`       | Delete a task              | Yes           |

### Example Payloads

#### Create Task (POST `/tasks`)

```json
{
  "title": "New Task",
  "description": "Details of the task"
}
```

#### Update Task (PUT `/tasks/{task_id}`)

```json
{
  "title": "Updated Task Title",
  "description": "Updated task details"
}
```

---

## IP, Country, and Weather Logging

For each API call, the following information is logged into the `api_call_logs` table:

- **IP Address**: The IP address of the client making the request.
- **Country**: The country where the IP address is located.
- **Weather Condition**: The current weather in the client's country, fetched using the WeatherAPI.

This is handled through a custom FastAPI decorator that is applied to each route.

---

## Running with Docker

You can use Docker to run the entire project in containers. A `docker-compose.yml` file is provided to help with this.

### Steps to Run

1. Ensure Docker is installed.
2. Build and run the containers:

   ```bash
   docker-compose up --build
   ```

3. The FastAPI app will be available at `http://localhost:8000`.

### Docker Compose Overview

The `docker-compose.yml` includes services for:

- **app**: The FastAPI application.
- **db**: PostgreSQL database.

---

## Postman Collection

You can use the provided Postman collection to interact with the API.

### Importing Postman Collection

1. Open Postman.
2. Go to **File** > **Import**.
3. Select the file `fastapi_task_api.postman_collection.json` from the project folder.

The collection includes requests for:

- Creating tasks
- Getting all tasks
- Getting a task by ID
- Updating a task
- Deleting a task

---

## Environment Variables

The project relies on the following environment variables:

| Variable         | Description                                   |
|------------------|-----------------------------------------------|
| `DATABASE_URL`    | PostgreSQL database connection string         |
| `WEATHERAPI_KEY`  | API key for the WeatherAPI service            |
| `SECRET_KEY`      | Secret key used for OAuth2 and token signing  |

Make sure to configure these variables before running the application.

---

## License

This project is licensed under the MIT License.

---

### Included Files

- **Postman Collection**: [`fastapi_task_api.postman_collection.json`](./fastapi_task_api.postman_collection.json)
- **API Documentation**: Available via Swagger at `/docs` or ReDoc at `/redoc` when running the project.
