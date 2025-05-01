# main.py

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import sqlite3
from auth import create_session, get_current_user
from database import init_db

app = FastAPI()
templates = Jinja2Templates(directory="templates")

init_db()

# Login form (GET)
@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Login handler (POST)
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    conn = sqlite3.connect("idor.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        create_session(username)
        return RedirectResponse(url="/dashboard", status_code=302)
    return {"error": "Invalid credentials"}

# Dashboard page
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    username = get_current_user()
    if not username:
        return RedirectResponse(url="/login", status_code=302)

    # Query the database for the number of messages and their IDs for the current user
    conn = sqlite3.connect("idor.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT messages.id FROM messages
        JOIN users ON users.id = messages.user_id
        WHERE users.username = ?
    """, (username,))
    messages = cursor.fetchall()  # Fetch all message IDs
    conn.close()

    # Extract message IDs into a list
    message_ids = [message[0] for message in messages]

    # Pass the message count and IDs to the template
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "username": username,
        "message_count": len(message_ids),
        "message_ids": message_ids
    })

# View message by ID — here lies the IDOR vulnerability!
@app.get("/message/{message_id}", response_class=HTMLResponse)
def read_message(request: Request, message_id: int):
    username = get_current_user()
    if not username:
        return RedirectResponse(url="/login", status_code=302)

    # Vulnerable: no access control
    conn = sqlite3.connect("idor.db")
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM messages WHERE id = ?", (message_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return templates.TemplateResponse("message.html", {"request": request, "message": row[0]})
    return {"error": "Message not found"}



# Secure version of the read_message function
# This version checks if the current user owns the message before displaying it.

# @app.get("/message/{message_id}", response_class=HTMLResponse)
# def read_message(request: Request, message_id: int):
#     username = get_current_user()
#     if not username:
#         return RedirectResponse(url="/login", status_code=302)

#     # Secure: Check if the current user owns the message
#     conn = sqlite3.connect("idor.db")
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT content FROM messages
#         JOIN users ON users.id = messages.user_id
#         WHERE messages.id = ? AND users.username = ?
#     """, (message_id, username))
    
#     row = cursor.fetchone()
#     conn.close()

#     if row:
#         return templates.TemplateResponse("message.html", {"request": request, "message": row[0]})
#     return templates.TemplateResponse("error.html", {"request": request, "detail": "Message not found or access denied"})
