# 📚 FastAPI Vulnerable App Collection

This repository contains intentionally vulnerable **FastAPI** applications designed for **educational purposes** in cybersecurity workshops and training sessions. Each app demonstrates a specific common web vulnerability.

> ⚠️ **Warning:** These applications are intentionally insecure. Do **not** deploy them in production environments.

---

## 🧪 Vulnerabilities Covered

- ✅ Cross-Site Scripting (XSS)
- ✅ SQL Injection (SQLi)
- ✅ Insecure Direct Object References (IDOR)
- ✅ Command Injection
- ✅ Cross-Site Request Forgery (CSRF)

---

## 🚀 Getting Started

1. **Clone the repository**
   
2. **Install dependencies:**
   ```bash
    pip install -r requirements.txt

3. **Run a demo (eg sqli):**
   ```bash
    uvicorn sqli.main:app --reload

4. **Visit the app in your browser:**
    ```arduino
      http://localhost:8000