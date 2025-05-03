from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import bleach


app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/submit", response_class=HTMLResponse)
async def submit_form(request: Request, comment: str = Form(...)):
    return templates.TemplateResponse("thank_you.html", {"request": request, "comment": comment})


# We use Bleach to sanitize user input before displaying it on the page.
# This prevents attackers from injecting malicious scripts (XSS attacks).
# Bleach removes or escapes dangerous HTML tags like <script>, while allowing safe ones if needed (like <b> or <i>).
# Without Bleach (or proper escaping), user input could run as code in the browser and harm users.

# solution is the following


# @app.post("/submit", response_class=HTMLResponse)
# async def submit(request: Request, comment: str = Form(...)):
#     clean_comment = bleach.clean(comment)
#     return templates.TemplateResponse("thank_you.html", {"request": request, "comment": clean_comment})
