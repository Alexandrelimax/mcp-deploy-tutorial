from fastmcp.server import FastMCP
from typing import Dict, Any
import httpx

mcp = FastMCP("MCP Rick and Morty API")

@mcp.tool(description="Buscar episódios da API Rick and Morty")
async def get_episodes(episode_id: int) -> Dict[str, Any]:
    """
    Busca e retorna os dados de um episódio específico da API Rick and Morty.

    Faz uma requisição GET assíncrona para a API Rick and Morty.

    Returns:
        Dict[str, Any]: Um dicionário contendo os dados do episódio.
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

    Faz uma requisição GET assíncrona para a API Rick and Morty.
    
    Args:
        character_id (int): O ID do personagem a ser buscado.
        
    Returns:
        Dict[str, Any]: Um dicionário contendo os dados do personagem.
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
