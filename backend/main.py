from fastapi import FastAPI

app = FastAPI()  # Creates the FASTAPI object kinda like our server


# Fast API turns functions into API endpoints
# We can use the wrapper to expose the python code through a seb server
@app.get("/")  # This is our first endpoint and is kinda like our homepage of the API
def health_check():  # This function is called when we trigger this route
    return {"status": "i'm alive"}
