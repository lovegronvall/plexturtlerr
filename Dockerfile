FROM python:3.11
WORKDIR /app
COPY requirements.txt .
COPY turtlerr.py .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "turtlerr.py"]

