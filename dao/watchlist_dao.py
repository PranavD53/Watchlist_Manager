from config import supabase

class WatchlistDAO:
    def __init__(self):
        self.supabase = supabase
        self.table = "userwatchlist"

    def add_to_watchlist(self, user_id: str, movie_id: str, status: str = "planning", rating: int = None, review: str = None):
        return self.supabase.table(self.table).insert({
            "user_id": user_id,
            "movie_id": movie_id,
            "status": status,
            "rating": rating,
            "review": review
        }).execute().data

    def get_watchlist_entry(self, watchlist_id: str):
        return self.supabase.table(self.table).select("*").eq("watchlist_id", watchlist_id).execute().data

    def get_user_watchlist(self, user_id: str):
        return self.supabase.table(self.table).select("*").eq("user_id", user_id).execute().data

    def get_user_watchlist_by_status(self, user_id: str, status: str):
        return self.supabase.table(self.table).select("*").eq("user_id", user_id).eq("status", status).execute().data

    def get_user_watchlist_by_genre(self, user_id: str, genre: str):
        return (self.supabase.table(self.table).select("*, movies_shows(title, genre)").eq("user_id", user_id).eq("movies_shows.genre", genre).execute().data)


    def update_watchlist_entry(self, watchlist_id: str, status: str = None, rating: int = None, review: str = None):
        update_fields = {}
        if status:
            update_fields["status"] = status
        if rating is not None:
            update_fields["rating"] = rating
        if review:
            update_fields["review"] = review

        if not update_fields:
            return {"error": "No fields to update"}

        return self.supabase.table(self.table).update(update_fields).eq("watchlist_id", watchlist_id).execute().data

    def remove_from_watchlist(self, watchlist_id: str):
        return self.supabase.table(self.table).delete().eq("watchlist_id", watchlist_id).execute().data


