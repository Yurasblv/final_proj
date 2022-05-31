FROM python:3.10
MAINTAINER "yurasblv.y@gmail.com"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /flaskapi
COPY requirements.txt /flaskapi
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /flaskapi
ENV FLASK_ENV=development
ENV FLASK_APP=run.py
EXPOSE 5000
CMD ["flask","run","--host=0.0.0.0"]
