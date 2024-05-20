from http.client import HTTPException
import aiohttp

BASE_URL = "https://www.buda.com/api/v2"


class BudaAPIActions:

    @staticmethod
    async def get_markets():
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{BASE_URL}/markets") as response:
                    response.raise_for_status()
                    markets = await response.json()
                    return markets
            except aiohttp.ClientResponseError as e:
                raise HTTPException(
                    status_code=e.status,
                    detail=f"Error al obtener mercados: {e.message}",
                )
            except aiohttp.ClientError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error de cliente al obtener mercados: {str(e)}",
                )
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error inesperado: {str(e)}",
                )
