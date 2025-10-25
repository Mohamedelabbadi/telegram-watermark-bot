# Use Python 3.11 slim to avoid imghdr issues
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg libglib2.0-0 libsm6 libxext6 libxrender-dev

# Copy requirements & install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy bot code & JSON files
COPY . .

# Environment variable TOKEN
ENV TOKEN=YOUR_BOT_TOKEN

# Start bot
CMD ["python", "bot.py"]
