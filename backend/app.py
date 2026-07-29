# Built by WanderingHippopotomus

import os
import tkinter as tk
from tkinter import filedialog

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.sorter import create_dir, sort_main
from backend.utils.time import time_to_run
from backend.logger import logger


app = FastAPI(title="File Sorter API")

# Allow React to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SortRequest(BaseModel):
    directory: str


@app.get("/api/default-dir")
def default_directory():
    downloads = os.path.join(
        os.path.expanduser("~"),
        "Downloads"
    )

    return {
        "path": downloads
    }


@app.get("/api/browse")
def browse_folder():
    """
    Opens a native folder picker.
    """

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    folder = filedialog.askdirectory()

    root.destroy()

    return {
        "path": folder
    }


@app.post("/api/sort")
def sort(request: SortRequest):

    directory = request.directory.strip()

    if directory == "":
        directory = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )

    if not os.path.isdir(directory):
        raise HTTPException(
            status_code=404,
            detail="Directory not found."
        )

    logger.info(f"Sorting directory: {directory}")

    os.chdir(directory)

    create_dir()

    runtime, result = time_to_run(
        lambda: sort_main(directory)
    )

    result["duration"] = runtime

    return result

import socket
import json
import uvicorn

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]
    
if __name__ == "__main__":
    port = find_free_port()
    print(f"PORT:{port}", flush=True)
    uvicorn.run(app, host="127.0.0.1", port=port)