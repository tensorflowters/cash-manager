FROM python:3.9
# enviroment

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

# RUN apt-get update && apt-get install nginx -y

# RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

WORKDIR /app

COPY . .

RUN pip install --upgrade pip  

RUN make install

EXPOSE 8000 