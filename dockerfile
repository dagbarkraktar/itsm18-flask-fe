FROM tiangolo/uwsgi-nginx-flask:python3.7

# Install packages
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY ./app /app


#FROM tiangolo/uwsgi-nginx-flask:python3.7
# Install packages
#RUN pip install Flask-SQLAlchemy==2.4.1
#RUN pip install mysql-connector-python==8.0.18
#RUN pip install redis==3.3.11
#RUN pip install requests==2.22.0
#COPY ./app /app