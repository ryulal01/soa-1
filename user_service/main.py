from fastapi import FastAPI
from database import engine, Base
import routes

app = FastAPI()


Base.metadata.create_all(bind=engine)

app.include_router(routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

