FROM python:3.13
WORKDIR /app
COPY requirements.txt .
COPY turtlerr.py .
RUN mkdir -p /config
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "turtlerr.py"]

