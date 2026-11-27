ARG BASE_IMAGE
FROM ${BASE_IMAGE:-undefined}

WORKDIR /opt/word_games

ARG UID
ARG GUID
RUN groupadd -g ${GUID} default_group \
    && useradd -m -u ${UID} -g default_group default_user

# Xvfb and Mesa give Kivy an invisible display with software OpenGL, so
# widget tests can create a window in this headless container.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    xvfb \
    xauth \
    libgl1 \
    libgl1-mesa-dri \
    libegl1 \
    && rm -rf /var/lib/apt/lists/*

ARG PIP_VERSION
ARG UV_VERSION
RUN pip --version \
    && pip install --no-cache-dir pip==${PIP_VERSION} \
    && pip --version \
    && pip install uv==${UV_VERSION} \
    && uv --version

# 1. Install only dependencies (cached layer while the lockfile is unchanged)
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project

# 2. Install the project
COPY . .
RUN uv sync --locked

RUN chown -R ${UID}:${GUID} .
USER default_user

CMD ["CMD must be overriden during container instantiation."]
