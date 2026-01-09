# 基于官方 Python 3.14 slim (trixie) 镜像
FROM python:3.14.0-slim-trixie

# 设置构建参数（代理等）
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG ALL_PROXY

# 安装必要工具，并创建 vscode 用户（UID/GID 1000）与 sudo
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        zsh git curl wget ca-certificates sudo passwd locales openssh-client \
     && rm -rf /var/lib/apt/lists/* \
    && groupadd -g 1000 vscode \
    && useradd -m -s /usr/bin/zsh -u 1000 -g 1000 vscode \
    && usermod -aG sudo vscode \
    && echo "vscode ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-vscode \
    && chmod 0440 /etc/sudoers.d/90-vscode

# 以 vscode 用户安装 oh-my-zsh（不自动进入 zsh）
USER vscode
ENV RUNZSH=no
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# Ensure container locale is UTF-8 so terminals and tools display non-ASCII correctly.
# Use C.UTF-8 which is commonly available in Debian-based slim images.
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Generate locale (if not present) to avoid setlocale warnings at runtime.
RUN sudo locale-gen C.UTF-8 || true

# 安装 uv 包管理器（到用户本地目录）并加入 PATH；同时使用独立安装器安装 ruff
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && curl -LsSf https://astral.ac.cn/ruff/install.sh | sh
ENV PATH="/home/vscode/.local/bin:${PATH}"

# 配置 Git 用户信息（可通过构建参数覆盖）并安装 Ruff CLI
ARG GIT_USER_NAME="par4d15e"
ARG GIT_USER_EMAIL="ericshen0911@163.com"
RUN git config --global user.name "${GIT_USER_NAME}" \
    && git config --global user.email "${GIT_USER_EMAIL}"

# 添加 VS Code Python 自动激活配置到 .zshrc
RUN echo '\n# >>> vscode python\nif [ -z "$VSCODE_PYTHON_AUTOACTIVATE_GUARD" ]; then\n    export VSCODE_PYTHON_AUTOACTIVATE_GUARD=1\n    if [ -n "$VSCODE_PYTHON_ZSH_ACTIVATE" ] && [ "$TERM_PROGRAM" = "vscode" ]; then\n        eval "$VSCODE_PYTHON_ZSH_ACTIVATE" || true\n    fi\nfi\n' >> /home/vscode/.zshrc

# 设置工作目录
WORKDIR /workspaces/fastapi_study

# 容器启动时的默认命令
CMD ["/bin/zsh"]
