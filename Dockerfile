FROM python:3-slim
WORKDIR /app
COPY server.py .
RUN mkdir -p data
RUN pip install flask gunicorn
CMD ["gunicorn", "-w", "8", "-b", "0.0.0.0:80", "--capture-output", "server:app"]