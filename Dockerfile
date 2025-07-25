FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose port 5000 (or the port your Flask app uses)
EXPOSE 5000

# Command to run the Flask app with Gunicorn
CMD ["gunicorn", "backend.app:app", "--bind", "0.0.0.0:5000"]
