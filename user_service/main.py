from fastapi import FastAPI
from database import engine, Base
import routes

app = FastAPI()



app.include_router(routes.router)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

