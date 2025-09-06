from fastapi import FastAPI, Request
import httpx
from routers import analytics_router

app = FastAPI()
app.include_router(analytics_router.router, prefix="/analytics")

USER_SERVICE_URL = "http://user_service:8000"

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        method = request.method
        url = f"{USER_SERVICE_URL}/{path}"
        headers = dict(request.headers)
        data = await request.body()
        response = await client.request(method, url, headers=headers, content=data)
        return response.json()

