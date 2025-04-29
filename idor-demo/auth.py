sessions = {}

def create_session(username: str):
    sessions["current_user"] = username

def get_current_user():
    return sessions.get("current_user", None)
