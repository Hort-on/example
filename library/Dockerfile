FROM python:3.11

WORKDIR /app

ADD . /app

ENV VIRTUAL_ENV "/venv"
RUN python -m venv $VIRTUAL_ENV
ENV PATH "$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt

RUN pip freeze

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]