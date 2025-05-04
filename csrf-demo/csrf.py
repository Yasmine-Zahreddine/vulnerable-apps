import secrets

csrf_tokens = {}

def generate_csrf_token(username: str) -> str:
    token = secrets.token_hex(16)
    csrf_tokens[username] = token
    return token

def validate_csrf_token(username: str, token: str) -> bool:
    return csrf_tokens.get(username) == token
