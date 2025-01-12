# Use an official Python runtime as the base image
FROM python:3.9-slim

# Accept SQL Server EULA
ENV ACCEPT_EULA=Y

# Install system dependencies for pyodbc and SQL Server drivers
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    curl gcc g++ gnupg unixodbc-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends msodbcsql17 mssql-tools \
    && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc \
    && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy project files into the container
COPY . .

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Verify pyodbc is installed
RUN python -c "import pyodbc; print('pyodbc installed successfully!')"

# Clean up unnecessary files
RUN apt-get clean

# Expose the application port
EXPOSE 8000

# Define the command to run the app
CMD ["python", "app.py"]
