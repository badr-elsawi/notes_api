FROM ubuntu
RUN apt update
RUN apt install python3-pip -y
RUN pip3 install flask
RUN pip3 install flask-restful
RUN pip3 install flask-sqlalchemy
RUN pip3 install flask-cors
WORKDIR /app
COPY . .
CMD ["python3","/app/notes_api.py"]