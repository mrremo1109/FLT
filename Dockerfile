FROM python:3.9

ENV FLASK_APP=app

# Create work directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

USER appuser

# Copy application code
COPY . .

# Expose Flask port
EXPOSE 5000

USER root
RUN chown -R appuser:appuser /app
RUN chmod -R 755 /app

USER appuser
RUN python3 init_db.py

CMD ["flask", "run", "--host=0.0.0.0"]