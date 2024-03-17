FROM python:3.9.18

COPY . /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app/FastApi

EXPOSE 54358

CMD ["uvicorn", "FastApi.main:app", "--host", "0.0.0.0", "--reload", "--port", "54358"]
