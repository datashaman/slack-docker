FROM python:3.6-alpine

WORKDIR /var/app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY app.py .

VOLUME [ "/var/app/config.yml", "/var/run/docker.sock"]

CMD ["python3", "app.py"]
