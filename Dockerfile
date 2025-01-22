FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip nodejs

WORKDIR /work
COPY . /work
RUN python -m venv .venv

RUN source .venv/bin/activate
RUN pip install -r requirements.txt

RUN npm --prefix music_recognition_web_portal install
RUN npm --prefix music_recognition_web_portal run build
RUN node --prefix music_recognition_web_portal/build
