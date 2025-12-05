
############################
# 1) Test Stage (dev)
############################
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim AS test


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

ENV VENV_PATH=/opt/venv
RUN python -m venv ${VENV_PATH}
ENV PATH="${VENV_PATH}/bin:${PATH}"

WORKDIR /app


COPY pyproject.toml README.md ./


COPY src ./src
COPY tests ./tests

RUN pip install --upgrade pip && \
    pip install -e .[dev]


RUN pytest


############################
# 2) Runtime Stage (minimal)
############################
FROM python:${PYTHON_VERSION}-slim AS runtime

ENV VENV_PATH=/opt/venv
RUN python -m venv ${VENV_PATH}
ENV PATH="${VENV_PATH}/bin:${PATH}"

WORKDIR /app


COPY pyproject.toml README.md ./
COPY src ./src


RUN pip install --upgrade pip && \
    pip install .


RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

ENTRYPOINT ["mastermind"]
CMD []