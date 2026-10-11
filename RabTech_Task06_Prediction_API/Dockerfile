FROM python:3.11.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY RabTech_Task06_Prediction_API/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY RabTech_Task06_Prediction_API/app.py ./app.py
COPY RabTech_Task03_Deliverables/clean_dataset.csv ./data/clean_dataset.csv

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)"

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
