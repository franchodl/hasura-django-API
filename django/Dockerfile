FROM python:3.9
ENV PIP_NO_CACHE_DIR=1
RUN pip install --upgrade pip
WORKDIR /code
ADD ./entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]