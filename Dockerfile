FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /DT2
RUN mkdir /DT2/staticfiles
RUN mkdir /DT2/media
WORKDIR /DT2
ADD requirements.txt /DT2/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
ADD . /DT2/
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y