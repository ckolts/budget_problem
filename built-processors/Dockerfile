FROM python:3.8-buster
WORKDIR /opt/src
ENV PYTHONPATH=/opt/src

RUN pip install pytest requests responses

COPY . /opt/src/

CMD [ "python", "-m", "built_processors.draw_processor" ]

