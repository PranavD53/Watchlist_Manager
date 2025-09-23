from config import supabase

class TitleDAO:
    def __init__(self):
        self.supabase = supabase
        self.table = "movies_shows"

    def add_title(self, title: str, type_: str, genre=None):
        return self.supabase.table(self.table).insert({
            "title": title,
            "type": type_,
            "genre": genre
        }).execute().data

    def get_title_by_id(self, movie_id: str):
        return self.supabase.table(self.table).select("*").eq("movie_id", movie_id).execute().data

    def list_titles(self):
        return self.supabase.table(self.table).select("*").execute().data

    def search_titles(self, keyword: str):
        return self.supabase.table(self.table).select("*").ilike("title", f"%{keyword}%").execute().data

    def update_title(self, movie_id: str, title: str = None, type_: str = None):
        update_fields = {}
        if title:
            update_fields["title"] = title
        if type_:
            update_fields["type"] = type_
        if not update_fields:
            return {"error": "No fields to update"}
        return self.supabase.table(self.table).update(update_fields).eq("movie_id", movie_id).execute().data

    def delete_title(self, movie_id: str):
        return self.supabase.table(self.table).delete().eq("movie_id", movie_id).execute().data
    
    def list_genres(self):
        response = supabase.table(self.table).select("genre").execute()
        genres = [row["genre"] for row in response.data if row.get("genre")]
        return list(set(genres))  

    
    def search_movies(self, query):
        response = supabase.table(self.table).select("*").or_(
            f"title.ilike.%{query}%,genre.ilike.%{query}%"
        ).execute()
        return response.data