FROM python:3.11.4-alpine
LABEL authors="Mafan"

ENTRYPOINT ["top", "-b"]

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

#COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

COPY . /usr/src/app

#ENTRYPOINT ["/usr/src/entrypoint.sh"]
