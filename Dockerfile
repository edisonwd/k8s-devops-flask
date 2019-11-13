FROM python:3.6
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip && pip install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "manage:app", "-c", "./gunicorn.conf.py"]