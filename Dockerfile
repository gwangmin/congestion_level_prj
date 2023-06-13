# pull official base image
FROM continuumio/miniconda3:22.11.1

# set work directory
WORKDIR /usr/src/app

# set environment variable
ENV PYTHONDONTWRTIEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY . /usr/src/app

# install dependencies
RUN conda install django -y
RUN pip install pillow
RUN pip install django-cleanup
RUN pip install gunicorn
# RUN python manage.py collectstatic
