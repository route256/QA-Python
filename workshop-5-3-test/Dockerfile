FROM python:3.10

# ARG ENV_FROM_GITLAB
# ENV ALLURE_TOKEN=$ALLURE_TOKEN

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt && \
    pip list

ENV PYTHONPATH=/app
