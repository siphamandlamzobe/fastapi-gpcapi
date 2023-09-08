from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from app.api import auth
from app.api.dependencies.database import database
from app.api.v1.api import api_router

app = FastAPI(title="Service Report API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
app.include_router(auth.router, tags=["Token"])


@app.on_event("startup")
async def startup() -> None:
    database_ = database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = database
    if database_.is_connected:
        await database_.disconnect()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
