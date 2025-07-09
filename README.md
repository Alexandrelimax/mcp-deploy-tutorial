# 🚀 FastMCP 2.0 — Tutorial explicativo

Este repositório mostra **como instalar, configurar e executar** um servidor **FastMCP** com **uv**, do zero, rodar localmente ou em produção (ex: Cloud Run).


## 📌 O que é o **uv**

**`uv`** é um **gerenciador de pacotes** ultrarrápido para Python, escrito em **Rust**.  
Ele substitui `pip` e `venv` com **sincronização de dependências**, **lockfile** (`uv.lock`) e instalação muito mais rápida.

🔗 [Mais sobre o uv](https://docs.astral.sh/uv/)

---

## ⚙️ Instalação do `uv`

Instale o `uv` globalmente usando `curl`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
ou no windows

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Verifique se o uv está instalado:

```bash
uv --version
```

## ⚙️ Instalar o FastMCP

Adicione o `FastMCP` como dependência do seu projeto usando uv:

```bash
uv add fastmcp
```
Ou, se preferir, instale diretamente:

```bash
uv pip install fastmcp
```
Verifique a versão instalada:

```bash
fastmcp version
```
Exemplo de saída:
```yaml
FastMCP version:   2.10.2
MCP version:       1.10.1
Python version:    3.12.2
```
---

## ✅ **Código principal**

```python
from fastmcp.server import FastMCP
from typing import Dict, Any
import httpx

mcp = FastMCP("MCP Rick and Morty API")

@mcp.tool(description="Buscar episódios da API Rick and Morty")
async def get_episodes(episode_id: int) -> Dict[str, Any]:
    """
    Busca e retorna os dados de um episódio específico da API Rick and Morty.
    """
    url = f"https://rickandmortyapi.com/api/episode/{episode_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "id": data.get("id"),
            "name": data.get("name"),
            "air_date": data.get("air_date"),
            "episode": data.get("episode"),
        }

@mcp.tool(description="Buscar personagem da API Rick and Morty")
async def get_character(character_id: int) -> Dict[str, Any]:
    """
    Busca e retorna os dados de um personagem específico da API Rick and Morty.
    """
    url = f"https://rickandmortyapi.com/api/character/{character_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "id": data.get("id"),
            "name": data.get("name"),
            "status": data.get("status"),
            "species": data.get("species"),
            "type": data.get("type"),
            "gender": data.get("gender"),
            "episode": data.get("episode", []),
            "location": data.get("location", {}),
        }

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8000, host="0.0.0.0")
```

## ✅ Explicação do código

1️⃣ Importações

- `FastMCP` é a classe principal do servidor.
- `httpx` é usado para fazer chamadas HTTP assíncronas à API Rick and Morty.

2️⃣ Instância

`mcp = FastMCP("MCP Rick and Morty API")`

Dá um nome amigável ao seu servidor MCP.

3️⃣ Tools (@mcp.tool)

São funções decoradas com @mcp.tool que o cliente MCP pode chamar para executar ações, acessar APIs externas, consultar dados ou realizar operações de forma controlada.

- Cada ferramenta fica exposta no contrato do MCP.
- O cliente (ex: um orquestrador, outro agente ou um LLM) chama essas funções como capabilities.
- São documentadas, tipadas e invocáveis de forma padronizada pelo Model Context Protocol

4️⃣ Execução

No bloco `if __name__ == "__main__":` rodamos `mcp.run()` para iniciar o servidor MCP.

---

📌 **Transports disponíveis**

✅ `stdio` (padrão):  
- Melhor opção para rodar localmente em ferramentas CLI ou integrando com clientes como Claude Desktop.
- Roda pelo terminal via entrada/saída padrão.
- Você NÃO expõe uma porta de rede.
- Exemplo:

```python
    from fastmcp import FastMCP

    mcp = FastMCP()

    if __name__ == "__main__":
        mcp.run(transport="stdio")
```

ℹ️ O `stdio` é o padrão — não precisa passar `transport="stdio"` se não quiser.  
Para testes locais no VSCode (`MCP: Add Server` → `Command (stdio)`), use `stdio`.

---

✅ `streamable-http` (ou `http`):  
- Recomendado para deploy web, produção, contêiner (ex: Cloud Run).
- Expõe o servidor via HTTP/REST + streaming.
- Usa `uvicorn` internamente.
- Exemplo:

```python
    from fastmcp import FastMCP

    mcp = FastMCP()

    if __name__ == "__main__":
        mcp.run(
            transport="streamable-http",
            host="0.0.0.0",
            port=8000
        )
```

⚠️ Use `host="0.0.0.0"` para que o contêiner aceite conexões externas.  
No `Dockerfile`, a porta deve bater com `EXPOSE`.

---

✅ `sse` (DEPRECATED):
- Baseado em Server-Sent Events (HTTP).
- Pode ser usado em ambientes legados.
- Nova recomendação: use `streamable-http` no lugar.
- Exemplo:
```python
    mcp.run(transport="sse")
```
---

✅ **Execução assíncrona**
Se seu app principal já é `async` (ex: rodando com `asyncio`), use `run_async()`:
```python
    import asyncio
    from fastmcp import FastMCP

    mcp = FastMCP()

    async def main():
        await mcp.run_async(transport="http")

    if __name__ == "__main__":
        asyncio.run(main())
```

⚠️ O `run()` cria seu próprio loop async, então **não chame `run()` dentro de uma função `async`** — use `run_async()` nesse caso.

---

📌 **Resumo**
- `stdio` → Ferramentas locais, plugins CLI.
- `streamable-http` → APIs, microserviços, deploy web.
- `sse` → Evite para novos projetos.
- Combine `transport`, `host`, `port` com o `EXPOSE` do Dockerfile.


---

✅ **Execução em modo dev com Inspector**

Para **desenvolvimento e testes**, o FastMCP fornece o comando `dev`, que executa o servidor e abre o **MCP Inspector**.

Isso permite inspecionar mensagens, testar chamadas de tools e verificar logs de interação.

📌 Exemplo:
```bash
    fastmcp dev main.py
```

ℹ️ O `main.py` é o arquivo que contém seu `FastMCP` — ajuste o nome conforme seu projeto.

Durante o `dev`:
- O servidor inicia com o transport padrão (`stdio` ou `streamable-http`).
- O Inspector abre localmente com uma URL, mostrando logs em tempo real.
- É a forma recomendada para testar tools de forma iterativa.

---

Use `fastmcp dev` sempre que precisar validar novas tools, endpoints ou integrações **localmente**, antes de fazer deploy no Cloud Run.

✅ **Execução MCP**

Além de `fastmcp dev`, você pode rodar seu servidor **direto** com:

- `uv run main.py`  
  Usa o `uv` como runner — carrega as dependências travadas (`pyproject.toml` + `uv.lock`).

- `fastmcp run main.py`  
  Usa o runner do próprio FastMCP.

---

✅ **Dockerfile — Como funciona**

Este `Dockerfile` faz tudo que seu **FastMCP** precisa para rodar **limpo e reprodutível** no Cloud Run (ou qualquer outro ambiente Docker).



🔹 **Imagem base**  
```dockerfile
FROM python:3.12-slim
```
Usa Python 3.12 em versão slim — imagem leve, rápida de build, ocupa pouco espaço.

---
🔹 **Diretório de trabalho**
```dockerfile
WORKDIR /app
```  
- Tudo que o contêiner fizer acontece dentro da pasta `/app`.
---

🔹 **Instala o uv**  
```dockerfile
RUN pip install uv
```
- O `uv` é um gerenciador de pacotes **ultrarrápido**, recomendado pelo **FastMCP**.
- Ele instala, sincroniza e congela as dependências de forma previsível.
---

🔹 **Copia as dependências**
```dockerfile
COPY pyproject.toml .
COPY uv.lock .
```  
- Copia os arquivos que definem **quais pacotes** instalar — `pyproject.toml` + `uv.lock`.
---

🔹 **Instala tudo**  
```dockerfile
RUN uv sync --frozen
```
- Instala **somente** as versões exatas travadas no `uv.lock`. Build idêntico, sem surpresas.
---

🔹 **Copia o código**
```dockerfile
COPY . .
```
- Traz seu `main.py` + demais arquivos pro contêiner.
---

🔹 **Porta**
```dockerfile
EXPOSE 8000
```
- Informa pro Cloud Run qual porta seu servidor usa — deve bater com `mcp.run(port=8000)`.
---

🔹 **Comando principal**
```dockerfile
CMD [ "uv", "run", "main.py" ]
```
- Quando o contêiner sobe, executa `uv run main.py`:
  - Usa o `uv` como runner.
  - Respeita o ambiente travado.
  - Sobe seu **FastMCP** na porta 8000.


📌 **Resumo**
- Imagem leve ✅
- Dependências travadas ✅
- Roteiro de build limpo ✅
- Pronto pro Cloud Run escalar ✅


---

**Pronto!**  
Com isso, seu projeto:
- Roda local (`fastmcp dev` ou `uv run`).
- Roda em produção (`Dockerfile` no Cloud Run).
- É rápido, consistente e seguro.

🚀 **MCP na nuvem, do jeito certo!**


✅ **Usando o VS Code como cliente MCP**

Depois de subir seu servidor MCP local ou em um serviço em nuvem, você pode **conectar o VS Code** como **cliente** usando o painel MCP.

Assim, você testa suas ferramentas (`@mcp.tool`) direto no **chat do Copilot**, **Claude** ou qualquer extensão MCP compatível.

---

🔹 **Passo 1 — Abrir o painel MCP**

No VS Code, pressione:
    *Ctrl + Shift + P*

E procure:
    *MCP: Add Server*

![mcp3](https://github.com/user-attachments/assets/77539394-a026-4ec2-b688-e34cd5307c18)

---

🔹 **Passo 2 — Escolher o tipo de servidor**

O VS Code mostra **estas opções** para adicionar seu servidor MCP 👇

---

🔹 **Command (stdio)**  
📌 Roda o MCP como um **processo local**, usando entrada/saída padrão (STDIO).  
✔️ Ideal pra dev local e plugins que gerenciam o processo.  
🗒️ Exemplo que aparecerá no settings.json: 
```json
{
  "mcp.servers": {
    "my-mcp": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "main.py"]
    }
  }
}
```

---

🔹 **HTTP (HTTP or Server-Sent Events)**  
📌 Conecta a um servidor MCP exposto via HTTP/SSE.  
✔️ Use se seu MCP roda com `transport="streamable-http"` (ou `http`).  
🗒️ Exemplo URL: `http://127.0.0.1:8000/mcp/`.

---

🔹 **NPM Package**  
📌 Instala um MCP distribuído como pacote **NPM** (Node.js).  
✔️ Útil pra MCPs mantidos como bots/plugins em JavaScript/TypeScript.

---

🔹 **Pip Package**  
📌 Instala um MCP direto do **PyPI** usando `pip`.  
✔️ Útil se você publica seu MCP como lib Python.  

---

🔹 **Docker Image**  
📌 Roda o MCP a partir de uma imagem Docker.  
✔️ Ideal para produção ou se você disponibilizar um contêiner pré-pronto.  
🗒️ Exemplo que aparecerá no settings.json: 
```json
{
    "Perplexity": {
      "type": "stdio",
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "PERPLEXITY_API_KEY", "mcp/perplexity-ask"],
      "env": {
        "PERPLEXITY_API_KEY": "${input:perplexity-key}"
    }
}
```
![mcp4](https://github.com/user-attachments/assets/cb37ba15-5612-4dbf-bc80-cbc06d0005a6)

---

🔹 **Passo 3 — Informar detalhes**

- Para **stdio**, informe o comando:
    uv run main.py
  ou
    fastmcp dev main.py

- Para **HTTP**, informe a URL:
    http://127.0.0.1:8000/mcp
  
![mcp5](https://github.com/user-attachments/assets/d368596d-01a5-45fe-8eee-53e9f6c3d4f8)

---

🔹 **Passo 4 — Dar nome ao servidor e verificar no painel**

Dê um **nome amigável** pro servidor — ex: `Rick and Morty MCP`.

![mcp6](https://github.com/user-attachments/assets/d34437ae-d31a-4d94-8b0c-11014ca8637d)

Depois de adicionar, seu servidor vai aparecer na lista de MCPs disponíveis no **Settings > MCP** do VS Code.

![mcp-edit](https://github.com/user-attachments/assets/27a70169-6f00-4163-8813-1a9b82ee30a2)

---

🔹 **Passo 5 — Testar**

Abra o **Copilot Chat** ou outra ferramenta compatível dentro do VS Code.  
Faça uma pergunta que chame sua `@mcp.tool` — ex:
    "Traga os detalhes do personagem ID 5 da API Rick and Morty"

O chat vai usar o seu **servidor MCP** como **ferramenta externa**.

---

### FIM

