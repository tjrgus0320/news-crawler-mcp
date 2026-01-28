FROM python:3.11-slim

WORKDIR /app

# Copy backend requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY backend/ ./backend/

WORKDIR /app/backend

# Railway uses PORT env variable
ENV PORT=8000
EXPOSE $PORT

# Run the application
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
