import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers.trip_router import router
from fastapi.responses import StreamingResponse

app = FastAPI(title="Travel Planner AI-Agent API")

# Get the absolute path of the directory containing main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Register your API router
app.include_router(router)

# Mount the static folder using the absolute path
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Serve the frontend HTML page on the root URL
@app.get("/")
async def serve_frontend():
    # Construct the absolute path to your index.html file
    index_path = os.path.join(STATIC_DIR, "index.html")
    return FileResponse(index_path)
