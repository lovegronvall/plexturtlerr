FROM python:3.11
WORKDIR /app
COPY requirements.txt .
COPY plex_turtlerr.py .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "plex_turtlerr.py"]

