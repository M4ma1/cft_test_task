FROM python:3.12

WORKDIR /worker

COPY . /worker/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "worker.py"]
