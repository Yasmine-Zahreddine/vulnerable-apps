def create_session(username: str):
    with open("session.txt", "w") as f:
        f.write(username)

def get_current_user():
    try:
        with open("session.txt", "r") as f:
            return f.read().strip()
    except:
        return None
