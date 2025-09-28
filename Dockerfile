FROM python:3.12-slim

WORKDIR /app

RUN echo "deb http://mirrors.aliyun.com/debian bookworm main contrib non-free non-free-firmware" > /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    apt-get update && apt-get install -y --no-install-recommends libzbar0 && \
    rm -rf /var/lib/apt/lists/*

# RUN apt-get update && apt-get install -y \
#     gcc \
#     libpq-dev \
#     libzbar0 \
#     zbar-tools \
#     && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync

COPY . .


EXPOSE 8000

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]