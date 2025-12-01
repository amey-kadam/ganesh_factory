# config.py
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    # PostgreSQL connection string
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:123@localhost:5432/ganesh_factory"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
