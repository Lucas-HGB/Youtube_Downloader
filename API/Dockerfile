FROM python:3.9
RUN mkdir /usr/src/youtube_downloader && mkdir /var/log/youtube_downloader && mkdir /etc/youtube_downloader && mkdir /var/lib/youtube_downloader
WORKDIR /usr/src/youtube_downloader
EXPOSE 8000
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY App/ .
CMD ["python", "-m", "uvicorn", "API:app", "--reload", "--port", "8000"]