"""
This dummy file is included only to have a default fallback app for a given service. 
Overwrite on your own and then set ENV in your dockerfile
"""

import sys

from fastapi import FastAPI

version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = FastAPI()


@app.get("/")
async def read_root():
    message = f"Hello world! From FastAPI running on Uvicorn with Gunicorn. Using Python {version}"
    return {"message": message}