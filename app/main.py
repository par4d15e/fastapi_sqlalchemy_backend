from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from app.core.database import engine
from app.api.v1.endpoints.heroes import router as heroes_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


def create_app() -> FastAPI:
    application = FastAPI(lifespan=lifespan)
    application.include_router(heroes_router)
    return application


app = create_app()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


def main() -> None:
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
