FROM python:3.12-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instala o `uv` globalmente (gerenciador de pacotes recomendado para fastmcp)
RUN pip install uv

# Copia o arquivo de dependências `pyproject.toml` para o contêiner
COPY pyproject.toml .

# Copia o arquivo de lock (trava versões exatas) para o contêiner
COPY uv.lock .

# Instala as dependências exatamente como definidas no `uv.lock`
RUN uv sync --frozen

# Copia o restante do código da aplicação para o contêiner
COPY . .

EXPOSE 8000

# Define o comando padrão para iniciar o servidor FastMCP
CMD [ "uv", "run", "main.py"]