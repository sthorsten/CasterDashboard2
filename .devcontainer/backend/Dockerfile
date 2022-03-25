FROM mcr.microsoft.com/vscode/devcontainers/python:3.9

# Install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN /root/.poetry/bin/poetry config virtualenvs.in-project true