FROM python:3.9

ENV FLASK_APP=app

# Create work directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Install dependencies
RUN pip install -r requirements.txt

USER appuser

# Copy application code
COPY . .

# Expose Flask port
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]