# 1. Use official Python base image
FROM python:3.10-slim

# 2. Set working directory inside the container
WORKDIR /app

# 3. Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. Install system dependencies first
RUN apt-get update && apt-get install -y \
    python3-dev \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && apt-get clean

# 5. Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 6. Copy project files
COPY . /app/

# 7. Expose port for Django
EXPOSE 8000

# 8. Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

