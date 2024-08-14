FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# Install build essentials and C++ compiler
RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get install -y g++ && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY src/deepllm /app/src/deepllm
COPY src/server /app/src/server
COPY bin/deepllm-fastapi /app/bin/deepllm-fastapi

# Give execution permissions to the script
RUN chmod +x /app/bin/deepllm-fastapi

# Expose port
EXPOSE 8000

# Set the script as the entry point
ENTRYPOINT ["/app/bin/deepllm-fastapi"]
