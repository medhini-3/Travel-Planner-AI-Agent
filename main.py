from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers.trip_router import router

app = FastAPI(title="Travel Planner AI-Agent API")

# Register your API router
app.include_router(router)

# Mount the static folder to serve CSS/JS if needed
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the frontend HTML page on the root URL
@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")