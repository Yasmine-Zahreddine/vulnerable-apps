from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from fastapi.staticfiles import StaticFiles
from typing import Optional

from auth import create_session, get_current_user
from database import init_db
from csrf import generate_csrf_token, validate_csrf_token



app = FastAPI()
templates = Jinja2Templates(directory="templates")
init_db()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    conn = sqlite3.connect("csrf.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        create_session(username)
        return RedirectResponse("/dashboard", status_code=302)
    return {"error": "Invalid credentials"}


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    username = get_current_user()
    if not username:
        return RedirectResponse("/login", status_code=302)

    conn = sqlite3.connect("csrf.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE username=?", (username,))
    balance = cursor.fetchone()[0]
    conn.close()

    return templates.TemplateResponse("dashboard.html", {"request": request, "username": username, "balance": balance})


@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("session_id")  # Example: Clear session cookie
    return response


# @app.get("/transfer", response_class=HTMLResponse)
def transfer_form(request: Request):
    username = get_current_user()
    if not username:
        return RedirectResponse("/login", status_code=302)

    return templates.TemplateResponse("transfer.html", {"request": request})


# @app.post("/transfer", response_class=HTMLResponse)
def transfer(request: Request, to_user: str = Form(...), amount: int = Form(...)):
    from_user = get_current_user()
    if not from_user:
        return RedirectResponse("/login", status_code=302)

    conn = sqlite3.connect("csrf.db")
    cursor = conn.cursor()

    # Deduct from sender
    cursor.execute("UPDATE users SET balance = balance - ? WHERE username = ?", (amount, from_user))
    # Add to recipient
    cursor.execute("UPDATE users SET balance = balance + ? WHERE username = ?", (amount, to_user))

    conn.commit()
    conn.close()
    return RedirectResponse("/dashboard", status_code=302)



# CSRF token generation and validation
# This is a secure way to generate a CSRF token

# Show transfer form with CSRF token
# @app.get("/transfer", response_class=HTMLResponse)
# def show_transfer_form(request: Request):
#     username = get_current_user()
#     if not username:
#         return RedirectResponse("/login", status_code=302)

#     csrf_token = generate_csrf_token(username)
#     return templates.TemplateResponse("transfer.html", {
#         "request": request,
#         "username": username,
#         "csrf_token": csrf_token
#     })

# Handle transfer POST with CSRF token validation
# @app.post("/transfer", response_class=HTMLResponse)
# def transfer_funds(request: Request, to_user: str = Form(...), amount: int = Form(...), csrf_token: Optional[str] = Form(None)):
#     username = get_current_user()
#     if not username:
#         return RedirectResponse("/login", status_code=302)

#     if not csrf_token or not validate_csrf_token(username, csrf_token):
#         return templates.TemplateResponse("error.html", {
#             "request": request,
#             "error_message": "Invalid CSRF token! Please try again."
#         })

#     conn = sqlite3.connect("csrf.db")
#     cursor = conn.cursor()

#     # Deduct from sender
#     cursor.execute("UPDATE users SET balance = balance - ? WHERE username = ?", (amount, username))
#     # Add to recipient
#     cursor.execute("UPDATE users SET balance = balance + ? WHERE username = ?", (amount, to_user))

#     conn.commit()
#     conn.close()
#     return RedirectResponse("/dashboard", status_code=302)

