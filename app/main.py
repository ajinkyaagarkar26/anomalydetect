from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import shutil, os
import deeplog
# from models.loganomaly import train_loganomaly

app = FastAPI()
UPLOAD_DIR = "app/uploads"
templates = Jinja2Templates(directory="app/templates")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": ""})

@app.post("/train/")
async def handle_train(request: Request, base_log: UploadFile = File(...), label_file: UploadFile = File(...)):
    log_path = os.path.join(UPLOAD_DIR, base_log.filename)
    label_path = os.path.join(UPLOAD_DIR, label_file.filename)

    with open(log_path, "wb") as f1:
        shutil.copyfileobj(base_log.file, f1)
    with open(label_path, "wb") as f2:
        shutil.copyfileobj(label_file.file, f2)

    # Run training scripts
    deeplog_result = deeplog.train()
    # loganomaly_result = train_loganomaly(log_path, label_path)

    # result_output = f"✅ DeepLog: {deeplog_result}<br>✅ LogAnomaly: {loganomaly_result}"
    result_output = f"✅ DeepLog: {deeplog_result}"
    return templates.TemplateResponse("index.html", {"request": request, "result": result_output})
