from fastapi import FastAPI, Request, Depends, HTTPException, status, Form, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import json
from pathlib import Path
from typing import Optional

from auth import authenticate_user, create_access_token, Config
from utils import DocumentProcessor
from gemini_agent import analyze_document

# Initialize FastAPI app
app = FastAPI(title="Legal Document Analysis System")

# Initialize document processor
doc_processor = DocumentProcessor(Config.UPLOAD_DIR)

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Initialize directories
Config.init_dirs()

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if authenticate_user(username, password):
        response = RedirectResponse(url="/upload", status_code=302)
        response.set_cookie(key="user", value=username)
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@router.get("/upload", response_class=HTMLResponse)
def upload_page(request: Request):
    docs = os.listdir(UPLOAD_DIR)
    return templates.TemplateResponse("upload.html", {"request": request, "docs": docs})

@router.post("/upload")
def upload_file(request: Request, file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return RedirectResponse(url="/upload", status_code=302)

@router.get("/review/{filename}", response_class=HTMLResponse)
def review_page(request: Request, filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    text = extract_text_from_word(file_path)
    return templates.TemplateResponse("review.html", {"request": request, "filename": filename, "text": text})

@router.post("/analyze/{filename}")
def analyze_file(request: Request, filename: str, domain: str = Form(...)):
    file_path = os.path.join(UPLOAD_DIR, filename)
    text = extract_text_from_word(file_path)
    result = call_gemini_api(text, domain)
    return RedirectResponse(url=f"/report/{filename}", status_code=302)

@router.get("/report/{filename}", response_class=HTMLResponse)
def report_page(request: Request, filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    text = extract_text_from_word(file_path)
    # For demo, call Gemini API with default domain
    result = call_gemini_api(text, "Finance and tax")
    return templates.TemplateResponse("report.html", {"request": request, "filename": filename, "result": result})
