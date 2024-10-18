FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

COPY . /home/ubuntu

RUN apt update && apt install -y pip

RUN pip install flask requests

WORKDIR /home/ubuntu

EXPOSE 5000

EXPOSE 65432

CMD ["sh", "-c", "python3 app.py & sleep 5; python3 simple_client_for_test.py"]
