from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import Base, engine
from routers import sections, posts, tags, auth



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting the app")
    Base.metadata.create_all(engine)
    yield
    print("Shutting down the app")


app = FastAPI(lifespan=lifespan)

app.mount("/public", StaticFiles(directory="public"), name="public")

app.include_router(sections.router)
app.include_router(posts.router)
app.include_router(tags.router)
app.include_router(auth.router)