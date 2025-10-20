# Dockerfile
FROM python:3.11-slim

# No need for ffmpeg if not a music bot
# RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Remove debugging lines as well
# RUN python -c "import audioop; print(f'audioop module found at: {audioop.__file__}')" || echo 'audioop module NOT found after pip install'
# RUN python -c "import sys; print(sys.path)"

# Copy the rest of your application code
COPY . .

# Define the command to run your bot
CMD ["python", "bot.py"]
