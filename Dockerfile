FROM python:3.9

WORKDIR /usr/src/app

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

COPY . /usr/src/app/

# Run the application.
CMD ["gunicorn","-w", "4", "--bind", "0.0.0.0:5050", "flaskwebsite:create_app()","--preload"]

