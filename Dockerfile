FROM node:22-alpine

RUN apk add --no-cache python3 py3-pip gcc

WORKDIR /work
COPY . /work
RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install -r requirements.txt

RUN cp /work/build.ts /work/music_recognition_web_portal/src/lib/build.ts
RUN npm --prefix music_recognition_web_portal install
RUN npm --prefix music_recognition_web_portal run build
EXPOSE 3000
CMD ["node", "music_recognition_web_portal/build"]
