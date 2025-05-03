from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = sqlite3.connect("db/users.db")
    cursor = conn.cursor()

    #  VULNERABLE TO SQL INJECTION!
    query = f"SELECT username, password FROM users WHERE username = '{username}' AND password = '{password}'"
    print(query)  
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    if result:
        return templates.TemplateResponse("welcome.html", {"request": request, "username": username})
    else:
        return HTMLResponse(content="Invalid login", status_code=401)



# This is the vulnerable code that allows SQL injection
# The following code is a demonstration of how to use parameterized queries to prevent SQL injection

# @app.post("/login", response_class=HTMLResponse)
# def login(request: Request, username: str = Form(...), password: str = Form(...)):
#     conn = sqlite3.connect("db/users.db")
#     cursor = conn.cursor()

#     # Using parameterized query
#     query = "SELECT * FROM users WHERE username = ? AND password = ?"
#     cursor.execute(query, (username, password))
#     result = cursor.fetchone()
#     conn.close()

#     if result:
#         return templates.TemplateResponse("welcome.html", {"request": request, "username": username})
#     else:
#         return HTMLResponse(content="Invalid login", status_code=401)