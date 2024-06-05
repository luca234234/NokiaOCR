FROM python:3.10

WORKDIR /usr/src/app/

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app/


CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5036"]

