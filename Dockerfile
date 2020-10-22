FROM python:latest

RUN apt-get update && apt-get install -y wait-for-it
WORKDIR /datadrive
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD wait-for-it --timeout=300 db:3306 -- flask run