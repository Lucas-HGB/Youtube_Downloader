FROM python:3.9
WORKDIR /app
EXPOSE 8000
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY App/ .
CMD ["python", "-m", "uvicorn", "API:app", "--port", "8000", "--host", "0.0.0.0"]