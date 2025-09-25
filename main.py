from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from web_routes import router as web_router

app = FastAPI(title="Legal Data Entry Automation AI Agent")
app.include_router(web_router)

# Mount static files if needed
# app.mount("/static", StaticFiles(directory="static"), name="static")

# To run: uvicorn main:app --reload
