FROM python:latest


RUN mkdir -p /home/app


ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY ./app/pyproject.toml .
COPY ./app/poetry.lock* .

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi 

COPY ./app $APP_HOME
COPY ./config $HOME

RUN chmod +x /home/app/entrypoint.sh

CMD [ "/home/app/entrypoint.sh" ]





# WORKDIR /app

# COPY ./app/pyproject.toml ./app/poetry.lock* /app/

# ENV PYTHONUNBUFFERED 1
# ENV PYTHONDONTWRITEBYTECODE 1

# # RUN apt-get update && \
# #     apt-get install -y 



# # COPY ./config/entrypoint.sh /app/

# # RUN sed -i 's/\r$//g' /app/entrypoint.sh
# # RUN chmod +x /app/entrypoint.sh

# COPY ./app /app/
# EXPOSE 8000
# CMD [ "python", "manage.py", "runserver", "--port", "8000" ]
# # ENTRYPOINT ["/app/entrypoint.sh"]


