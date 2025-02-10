# Python image
FROM python:3.9

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set working dir inside the container
WORKDIR /app
#COPY deuwo.py /app

COPY apartment_hunt /app/apartment_hunt

COPY ../requirements.txt /app/requirements.txt
COPY ../keys.json /app/keys.json

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "apartment_hunt.deuwo"]
