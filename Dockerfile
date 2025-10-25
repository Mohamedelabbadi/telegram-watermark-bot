# Use Python 3.11 slim
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (ffmpeg for MoviePy)
RUN apt-get update && apt-get install -y ffmpeg

# Copy requirements & install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all code
COPY . .

# Environment variable TOKEN
ENV TOKEN=YOUR_BOT_TOKEN

# Start bot
CMD ["python", "bot.py"]
