FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. glossary.proto

EXPOSE 50051

CMD ["python", "server.py"]
