FROM python:3.8.5


WORKDIR /app
# COPY Pipfile Pipfile.lock /app/
COPY . /app
RUN pip install pipenv

RUN  pipenv update;pipenv install --system --deploy
# RUN  pipenv install
EXPOSE 5000
CMD ["python", "app.py"]