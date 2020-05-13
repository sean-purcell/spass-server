FROM alpine:edge

WORKDIR /app

RUN apk --no-cache add bash python3 py3-pip uwsgi uwsgi-python3 libgcc libc6-compat
RUN pip3 install --trusted-host pypi.python.org --upgrade pip

RUN apk --no-cache add py3-wheel
ADD requirements.txt /app/
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

ADD server.py /app/
ADD spass /app/
ADD uwsgi.ini /app/
ADD nginx.conf /app/
ADD entry.sh /app/
ADD static/index.html /app/

# self-documentation
ADD Dockerfile /app/

EXPOSE 8000
EXPOSE 8001

ENTRYPOINT ["./entry.sh"]
