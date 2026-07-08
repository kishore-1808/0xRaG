import os
import json
import bcrypt
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict

USERS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")

def _load_users() -> Dict:
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def _save_users(users: Dict):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

def register_user(username: str, password: str) -> Dict:
    users = _load_users()
    if username in users:
        return {"success": False, "message": "Username already exists."}
    users[username] = {
        "password": hash_password(password),
        "created_at": datetime.now().isoformat(),
    }
    _save_users(users)
    return {"success": True, "message": "User registered successfully."}

def authenticate_user(username: str, password: str) -> Dict:
    users = _load_users()
    if username not in users:
        return {"success": False, "message": "Invalid username or password."}
    if not verify_password(password, users[username]["password"]):
        return {"success": False, "message": "Invalid username or password."}
    token = secrets.token_hex(32)
    return {"success": True, "message": "Login successful.", "token": token, "username": username}

def validate_token(token: str) -> Optional[str]:
    return None

def login_prompt() -> Optional[str]:
    print("\n--- Authentication Required ---")
    print("1. Login")
    print("2. Register")
    print("3. Continue as Guest")
    choice = input("\nSelect an option (1-3): ").strip()

    if choice == "1":
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        result = authenticate_user(username, password)
        if result["success"]:
            print(f"Welcome back, {username}!")
            return result["token"]
        else:
            print(result["message"])
            return None
    elif choice == "2":
        username = input("Choose a username: ").strip()
        password = input("Choose a password: ").strip()
        result = register_user(username, password)
        print(result["message"])
        if result["success"]:
            return authenticate_user(username, password)["token"]
        return None
    elif choice == "3":
        print("Continuing as guest. Some features may be limited.")
        return "guest"
    else:
        print("Invalid option.")
        return None
