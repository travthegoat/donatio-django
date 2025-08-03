FROM python:3.12

WORKDIR /app

# Replace Debian sources.list with Aliyun mirror for Debian 12 (Bookworm) and install dependencies
RUN echo "deb http://mirrors.aliyun.com/debian bookworm main contrib non-free non-free-firmware" > /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libcairo2-dev \
    pkg-config \
    libffi-dev \
    python3-dev \
    libgirepository1.0-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libzbar0 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements.txt and install Python dependencies with pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install uv environment manager
RUN pip install --no-cache-dir uv

# Copy pyproject.toml and sync uv dependencies (optional, only if you use uv environment management)
COPY pyproject.toml .
RUN uv sync
RUN uv add django-environ

# Copy the rest of your project files
COPY . .

EXPOSE 8000

# Run your Django management command through uv
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
