FROM ubuntu:24.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    # 基礎工具（原 devcontainers/base 提供）
    curl \
    ca-certificates \
    sudo \
    git \
    # 課程開發工具（參照 linux2025-lab0.md Part A）
    build-essential \
    valgrind \
    cppcheck \
    clang-format \
    wamerican \
    aspell \
    colordiff \
    && rm -rf /var/lib/apt/lists/*

# 建立 vscode 使用者（devcontainer 慣例）
RUN groupadd -g 1000 vscode \
    && useradd -m -s /bin/bash -u 1000 -g 1000 vscode \
    && echo "vscode ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/vscode

# uv + Python 3.12（以 vscode 使用者安裝）
USER vscode
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && ~/.local/bin/uv python install 3.12
USER root
