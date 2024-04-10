FROM tiangolo/uvicorn-gunicorn:python3.11

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app

RUN mkdir -p torrents/tmp

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8192"]
