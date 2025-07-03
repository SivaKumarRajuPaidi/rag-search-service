FROM python:3.11.8-slim-bookworm  

WORKDIR /app

# Update system packages for security patches
RUN apt-get update && apt-get upgrade -y --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
