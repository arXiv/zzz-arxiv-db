FROM python:3.8-slim
ARG git_commit

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc python3-dev default-libmysqlclient-dev

# Setup venv and put into use. https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV VIRTUAL_ENV=/opt/modapi-venv
RUN python3 -m venv $VIRTUAL_ENV

# Every python thing after this is in the venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python -m pip install -U pip

WORKDIR /opt/arxiv/
RUN pip install poetry

ADD poetry.lock /opt/arxiv/
ADD pyproject.toml /opt/arxiv/
RUN poetry install
RUN pip uninstall -y poetry 
 
RUN echo $git_commit > /git-commit.txt
ADD modapi /opt/arxiv/modapi

ENV SQLALCHEMY_TRACK_MODIFICATIONS False
EXPOSE 8000
CMD ["python", "-m", "modapi.app"]


