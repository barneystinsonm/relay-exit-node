FROM python:3.10-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

# هاگینگ فیس به صورت پیش‌فرض روی پورت 7860 کار می‌کند
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
