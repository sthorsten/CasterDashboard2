FROM python:3.10.5

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.1.13 \
&& /root/.local/bin/poetry config virtualenvs.in-project true

# Install dependencies
WORKDIR /backend
COPY ["pyproject.toml", "poetry.lock", "."]
RUN /root/.local/bin/poetry install

# Copy project files
COPY . .
COPY .env.docker .env