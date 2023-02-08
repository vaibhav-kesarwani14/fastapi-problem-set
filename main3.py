from typing import List

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse

app = FastAPI()


@app.post("/files/")
async def create_files(files: List[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile]):
    # read  = files.read()

    return {{"filenames": file.filename, "filenames": file.decode()} for file in files}


@app.get("/")
async def main():
    return FileResponse('index.html')
