FROM python:3.13 AS builder
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt -w /wheelhouse

FROM python:3.13
WORKDIR /app
COPY . .
COPY --from=builder /wheelhouse /wheelhouse
RUN pip install --no-index --find-links=/wheelhouse requirements.txt

CMD ["compress", "hello", "world"]