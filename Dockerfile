FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN addgroup --gid 10001 appgroup \
    && adduser --uid 10001 --ingroup appgroup --disabled-password --gecos "" --no-create-home appuser

COPY requirements.txt .
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

COPY app ./app

USER 10001:10001

EXPOSE 8080

CMD ["gunicorn", "--worker-tmp-dir", "/tmp", "--access-logfile", "-", "--error-logfile", "-", "-b", "0.0.0.0:8080", "app.main:app"]
