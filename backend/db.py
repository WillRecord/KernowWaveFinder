from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./backend.db"

# Create the engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite with FastAPI
    # to stop multi-threading errors
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models to allow for us to define SQLAlchemy ORM models
Base = declarative_base()


# Dependency injected into API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
