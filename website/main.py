from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

templates = Jinja2Templates(directory="template")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.get("/download")
def download():
    return FileResponse(
        os.path.join(BASE_DIR, "static", "File Sorter Setup 1.0.0.exe"),
        filename="FileSorterSetup.exe",
        media_type="application/octet-stream",
    )