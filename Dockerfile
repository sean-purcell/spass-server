FROM alpine:edge

WORKDIR /app

RUN apk --no-cache add bash python3 py3-pip uwsgi uwsgi-python3 libgcc libc6-compat nginx
RUN pip3 install --trusted-host pypi.python.org --upgrade pip

RUN apk --no-cache add py3-wheel
ADD requirements.txt /app/
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

ADD server.py /app/
ADD spass /app/
ADD uwsgi.ini /app/
ADD entry.sh /app/
ADD nginx.conf /etc/nginx/http.d/spass.conf

RUN mkdir -p /run/nginx
RUN mkdir -p /www
ADD static/index.html /www/index.html

# self-documentation
ADD Dockerfile /app/

EXPOSE 4480

ENTRYPOINT ["./entry.sh"]
