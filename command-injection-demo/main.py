from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import subprocess

app = FastAPI()
templates = Jinja2Templates(directory="templates")


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
# @app.post("/ping")
# def secure_ping(host: str = Form(...)):
#     try:
#         output = subprocess.check_output(
#             ["ping", "-c", "1", host],
#             stderr=subprocess.STDOUT,
#             timeout=5
#         )
#         return HTMLResponse(f"<pre>{output.decode()}</pre>")
#     except subprocess.CalledProcessError as e:
#         return HTMLResponse(f"<pre>Ping failed:\n{e.output.decode()}</pre>", status_code=400)
#     except subprocess.TimeoutExpired:
#         return HTMLResponse("<pre>Ping timed out</pre>", status_code=408)
