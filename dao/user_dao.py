from config import supabase

class UserDAO:
    def __init__(self):
        self.supabase = supabase
        self.table = "users"

    def create_user(self, name: str, email: str):
        return self.supabase.table(self.table).insert({
            "name": name,
            "email": email
        }).execute().data

    def get_user_by_id(self, user_id: str):
        return self.supabase.table(self.table).select("*").eq("user_id", user_id).execute().data

    def get_user_by_email(self, email: str):
        return self.supabase.table(self.table).select("*").eq("email", email).execute().data

    def list_users(self):
        return self.supabase.table(self.table).select("*").execute().data

    def update_user(self, user_id: str, name: str = None, email: str = None):
        update_fields = {}
        if name:
            update_fields["name"] = name
        if email:
            update_fields["email"] = email
        if not update_fields:
            return {"error": "No fields to update"}
        return self.supabase.table(self.table).update(update_fields).eq("user_id", user_id).execute().data

    def delete_user(self, user_id: str):
        return self.supabase.table(self.table).delete().eq("user_id", user_id).execute().data

