FROM python:3.8
RUN pip install poetry
COPY poetry.lock pyproject.toml /app/
EXPOSE 80
COPY ./ /app
WORKDIR /app
RUN  poetry install --no-dev
CMD ["poetry", "run", "uvicorn", "temapi.api:app", "--reload", "--host", "0.0.0.0", "--port", "80"]