from dao.user_dao import UserDAO

class UserService:
    def __init__(self):
        self.dao = UserDAO()

    def create_user(self, name: str, email: str):
        """Business rule: email must be unique"""
        existing = self.dao.get_user_by_email(email)
        if existing:
            return {"error": "Email already exists."}
        return self.dao.create_user(name, email)

    def get_user(self, user_id: str):
        """Fetch user details"""
        return self.dao.get_user_by_id(user_id)

    def list_users(self):
        """List all users"""
        return self.dao.list_users()

    def update_user(self, user_id: str, name: str = None, email: str = None):
        """Update user details"""
        if email:
            existing = self.dao.get_user_by_email(email)
            if existing and existing[0]["user_id"] != user_id:
                return {"error": "Email already in use by another user."}
        return self.dao.update_user(user_id, name, email)

    def delete_user(self, user_id: str):
        """Delete user and cascade their watchlist"""
        return self.dao.delete_user(user_id)


