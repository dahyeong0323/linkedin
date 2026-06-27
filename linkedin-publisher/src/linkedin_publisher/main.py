from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from linkedin_publisher.db import init_db
from linkedin_publisher.routes.auth import router as auth_router
from linkedin_publisher.routes.drafts import router as drafts_router
from linkedin_publisher.routes.publish import router as publish_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="LinkedIn Publisher", version="0.1.0", lifespan=lifespan)
templates_path = Path(__file__).parent / "templates"
app.state.templates = Jinja2Templates(directory=str(templates_path))
app.include_router(auth_router)
app.include_router(drafts_router)
app.include_router(publish_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
