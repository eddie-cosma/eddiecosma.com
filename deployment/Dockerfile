FROM tiangolo/uwsgi-nginx-flask:python3.11

RUN useradd -ms /bin/bash eddiecosma
RUN usermod -a -G eddiecosma nginx
RUN usermod -a -G eddiecosma www-data

COPY ./app/requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

COPY ./app /app

