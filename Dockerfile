# Get the base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project folder to the working directory
COPY . .

# Expose the ports for Streamlit and FastAPI
EXPOSE 8501 8000

# Run both Streamlit and FastAPI using a shell script
CMD ["sh", "./start_services.sh"]



