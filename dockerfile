
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY train.py app.py ./

RUN python train.py

EXPOSE 5000

ENV MODEL_VERSION=1.0

CMD ["python", "app.py"]
