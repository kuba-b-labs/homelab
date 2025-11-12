FROM python:3.13.9-alpine3.22


COPY . /dynamic-targets

WORKDIR /dynamic-targets

RUN pip install kubernetes

USER 65534

CMD ["python","main.py"]
