# Use the slim version of Python 3.11 for an optimized, small footprint (~45MB)
# It is much smaller than the standard python image but more compatible than alpine.
FROM python:3.11-slim

# Set environment variables to optimize Python behavior
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files (saves disk space)
# PYTHONUNBUFFERED: Ensures logs are output immediately without buffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy requirements FIRST to leverage Docker layer caching
# If requirements.txt doesn't change, Docker skips reinstalling dependencies
COPY requirements.txt .

# Install dependencies
# --no-cache-dir reduces the image size by discarding the pip downloaded archive files
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual application files
COPY app.py config.py ./

# Create a non-root user for better container security (Best Practice)
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose the application port
EXPOSE 5000

# Run the Flask server
CMD ["python", "app.py"]
