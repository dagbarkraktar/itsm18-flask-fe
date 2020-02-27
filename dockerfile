FROM tiangolo/uwsgi-nginx-flask:python3.7

# Install packages
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY ./app /app
