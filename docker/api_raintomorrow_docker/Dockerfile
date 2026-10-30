FROM python:3.10

WORKDIR /usr/src/app

COPY ./ ./

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "8000"]



