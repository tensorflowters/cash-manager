#syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /api
COPY requirements.txt /api/
RUN pip install -r requirements.txt
COPY . /api/
CMD ["python" , "manage.py",  "runserver", "0.0.0.0:8000"]
