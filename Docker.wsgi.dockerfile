FROM python:3.10
ENV PYTHONUNBURRERED 1

RUN mkdir /apps/

COPY ./src/ /apps/
COPY ./.env /apps/.env

WORKDIR /apps/

RUN pip install pip==21.3.1

RUN pip install poetry

RUN poetry export --without-hashes -f requirements.txt --output requirements.txt

RUN pip install -r requirements.txt

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
