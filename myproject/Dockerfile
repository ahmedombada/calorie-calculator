#you basically need to create an image out of this app
#step1: specify base image

FROM python:3

#step2: set enviromental variables
ENV PYTHONNUNBUFFERED 1
#step3: specify working directory
WORKDIR /tracker

#copy everything to the app directory
ADD . /tracker 

#INSTALL DEPENDANCIES FROM THE REQUIREMENTS.TXT (IF YOU DONT HAVE A FILE CALLED REUIREMENTS.TXT, CREATE ONE AND SET THE VERSIONS OF THE STUFF U NEED)
#THEN COPY THE FILE INTO THIS FILE USING 

COPY ./req.txt /tracker/requirements.txt

RUN pip install -r req.txt

COPY . /tracker
