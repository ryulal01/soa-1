import httpx

USER_SERVICE_URL = "http://user_service:8000"

async def forward_request(method: str, path: str, headers: dict, data: bytes):
    async with httpx.AsyncClient() as client:
        url = f"{USER_SERVICE_URL}/{path}"
        response = await client.request(method, url, headers=headers, content=data)
        return response.json()

