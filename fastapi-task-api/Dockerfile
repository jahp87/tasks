
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install PostgreSQL client for database communication
RUN apt-get update && apt-get install -y postgresql-client

# Expose the port the app runs on
EXPOSE 8000

# Set environment variables for database connection
ENV POSTGRES_USER=fastapi_user
ENV POSTGRES_PASSWORD=fastapi_password
ENV POSTGRES_DB=fastapi_db
ENV POSTGRES_HOST=db
ENV POSTGRES_PORT=5432

# Run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]