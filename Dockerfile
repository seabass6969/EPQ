FROM node:22-alpine

RUN apk add --no-cache python3 py3-pip ffmpeg

WORKDIR /work
COPY . /work
RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install -r requirements.txt

run cp /work/prod_build.ts /work/music_recognition_web_portal/src/lib/build.ts
run cp /work/prod_settings.py /work/music_recognition_main/settings.py

RUN npm --prefix music_recognition_web_portal install
RUN npm --prefix music_recognition_web_portal run build
EXPOSE 3000
CMD ["node", "music_recognition_web_portal/build"]
