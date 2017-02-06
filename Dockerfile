FROM python:2.7-wheezy

RUN apt-get update && apt-get install -y vim cron
ADD . /app/
RUN find /app -name "*.pyc" -type f -delete | xargs rm -rf
RUN pip install --process-dependency-links -r /app/requirements.txt
RUN crontab /app/crontab && cron
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["app.py"]