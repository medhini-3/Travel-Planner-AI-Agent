from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from routers.trip_router import router

app = FastAPI(title="Travel Planner AI-Agent API")

# Enable CORS so your frontend communicates seamlessly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register your API router with the correct /api/v1 prefix matching your frontend
app.include_router(router, prefix="/api/v1")

# Mount the static folder to serve CSS/JS if needed
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the frontend HTML page on the root URL
@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")