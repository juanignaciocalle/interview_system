FROM python:3.12-slim AS base

# Set timezone up to avoid tzdata configuration
ENV TZ=America/Argentina/Buenos_Aires
# echo $TZ > /etc/timezone
RUN rm -rf /etc/localtime && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential python3-opencv libdmtx0b iputils-ping \
    && rm -rf /var/lib/apt/lists/*
    

# ------------------------------------------------------------------------------
# Stage: Deploy
# ------------------------------------------------------------------------------
FROM base AS deploy

WORKDIR /workspace

# Copy the application
COPY . .


COPY requirements.txt /workspace/
RUN pip3 install -r requirements.txt
