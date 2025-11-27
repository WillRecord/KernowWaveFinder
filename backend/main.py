from fastapi import FastAPI
from backend.db import Base, engine
from backend import models
from backend.routes import surf
from backend.routes import cache

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()  # Creates the FASTAPI object kinda like our server


# Register API routes
app.include_router(cache.router)
app.include_router(surf.router)

# Fast API turns functions into API endpoints
# We can use the wrapper to expose the python code through a seb server

@app.get("/")  # This is our first endpoint and is kinda like our homepage of the API
def health_check():  # This func is called when we access url
    return {"status": "i'm alive"}
