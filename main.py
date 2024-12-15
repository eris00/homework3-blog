from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import sections, posts, tags, auth

app = FastAPI()

app.mount("/public", StaticFiles(directory="public"), name="public")

app.include_router(sections.router)
app.include_router(posts.router)
app.include_router(tags.router)
app.include_router(auth.router)