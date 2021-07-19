FROM python:3.8-slim-buster

ADD app.py app/app.py
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD ["/app/app.py"]
ENTRYPOINT ["python"]
