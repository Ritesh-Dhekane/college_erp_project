# Use Python 3.11
FROM python:3.11-slim

# Set work directory inside container
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Default command to run Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
