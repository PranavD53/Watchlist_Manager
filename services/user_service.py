from dao.user_dao import UserDAO
import hashlib

class UserService:
    def __init__(self):
        self.dao = UserDAO()

    def create_user(self, name: str, email: str):
        existing = self.dao.get_user_by_email(email)
        if existing:
            return {"error": "Email already exists."}
        return self.dao.create_user(name, email)

    def get_user(self, user_id: str):
        return self.dao.get_user_by_id(user_id)

    def list_users(self):
        return self.dao.list_users()

    def update_user(self, user_id: str, name: str = None, email: str = None):
        if email:
            existing = self.dao.get_user_by_email(email)
            if existing and existing[0]["user_id"] != user_id:
                return {"error": "Email already in use by another user."}
        return self.dao.update_user(user_id, name, email)

    def delete_user(self, user_id: str):
        return self.dao.delete_user(user_id)
    
    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, name: str, email: str, password: str):
        existing = self.dao.get_user_by_email(email)
        if existing:
            return {"error": "Email already exists."}
        return self.dao.create_user(name, email, self.hash_password(password))

    def authenticate_user(self, email: str, password: str):
        user = self.dao.get_user_by_email(email)
        if not user:
            return None
        if user[0]["password"] == self.hash_password(password):
            return user[0]
        return None

    def update_user(self, user_id: str, name: str = None, email: str = None, password: str = None):
        hashed_pw = self.hash_password(password) if password else None
        return self.dao.update_user(user_id, name, email, hashed_pw)

