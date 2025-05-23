from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os
import subprocess

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return RedirectResponse(url="/ping")


@app.get("/ping", response_class=HTMLResponse)
def get_ping_form(request: Request):
    return templates.TemplateResponse("ping.html", {"request": request})


# POST: Handle the ping request (vulnerable)
@app.post("/ping", response_class=HTMLResponse)
def ping_host(request: Request, host: str = Form(...)):
    command = f"ping -c 2 {host}"
    result = os.popen(command).read()
    return templates.TemplateResponse("result.html", {"request": request, "output": result})


# Split command into a list (no shell=True)
# This is a safer way to execute commands
# Adds a list for the command and arguments

# @app.post("/ping", response_class=HTMLResponse)
# def secure_ping(request: Request, host: str = Form(...)):
#     try:
#         output = subprocess.check_output(
#             ["ping", "-c", "1", host],
#             stderr=subprocess.STDOUT,
#             timeout=5
#         )
#         return templates.TemplateResponse("result.html", {"request": request, "output": output.decode()})
#     except subprocess.CalledProcessError as e:
#         return templates.TemplateResponse("result.html", {"request": request, "output": f"Ping failed:\n{e.output.decode()}"})
#     except subprocess.TimeoutExpired:
#         return templates.TemplateResponse("result.html", {"request": request, "output": "Ping timed out"})