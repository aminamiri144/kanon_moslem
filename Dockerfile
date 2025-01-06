FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE kanon_moslem.settings

WORKDIR /kanon_moslem

COPY requirements.txt /kanon_moslem/
RUN pip install -r requirements.txt
COPY . /kanon_moslem/
RUN mkdir -p /kanon_moslem/staticfiles

RUN python manage.py collectstatic
RUN python manage.py makemigrations
RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]