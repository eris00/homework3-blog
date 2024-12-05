from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:ebackender44@localhost/blog-project-t1"

    class Config:
        env_file = ".env"
