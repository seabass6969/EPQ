FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip nodejs npm

WORKDIR /work
COPY . /work
# RUN python3 -m venv .venv

# RUN source .venv/bin/activate
# I don't think it need virtual environment anyways
RUN pip install -r requirements.txt

RUN npm --prefix music_recognition_web_portal install
RUN npm --prefix music_recognition_web_portal run build
EXPOSE 3000
CMD ["node", "--prefix", "music_recognition_web_portal/build"]
