# Use a lightweight official Python base image
FROM python:3.11-slim

# Set environment variables for Python performance & terminal output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy dependency definition to leverage Docker build caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy source directories
COPY backend/ ./backend
COPY frontend/ ./frontend

# Expose FastAPI server port
EXPOSE 8000

# Execute server using uvicorn
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
