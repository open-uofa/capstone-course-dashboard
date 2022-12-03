# syntax=docker/dockerfile:1
FROM python:3.10

LABEL name="Capstone Dashboard Backend"
LABEL description="Hosts the FastAPI backend of Capstone Dashboard"

WORKDIR /app

# Required for numpy
#RUN apk --no-cache add g++

# Install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy server files
COPY . .

# Run server to accept all connections on port 80
EXPOSE 80
ENTRYPOINT ["uvicorn", "server.app:app"]
CMD ["--host=0.0.0.0", "--port=80"]
