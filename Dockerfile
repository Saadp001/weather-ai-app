# Use an official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 8000

# Run the app using gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
