from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from app.api.dependencies.database import database

from app.api.v1.endpoints import service_report, service_report_type

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(service_report.router, prefix="/v1", tags=["Version 1"])
app.include_router(service_report_type.router, prefix="/v1", tags=["Version 1"])


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
    uvicorn.run(app, host="0.0.0.0", port=8000)