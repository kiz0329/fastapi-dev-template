FROM python:3-3.14-trixie

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip3 --disable-pip-version-check --no-cache-dir install -r requirements.txt

COPY main.py ./main.py
COPY __project_name__ ./__project_name__

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]