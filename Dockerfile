# Use Python 3.11 slim to avoid imghdr issue
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements & install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all code
COPY . .

# Environment variable TOKEN will be set in Render
ENV TOKEN=YOUR_BOT_TOKEN

# Start bot
CMD ["python", "bot.py"]
