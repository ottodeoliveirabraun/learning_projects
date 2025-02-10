# Python image
FROM python:3.9

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set working dir inside the container
WORKDIR /app
COPY deuwo.py

COPY . /app

COPY ../requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "deuwo.py"]
