from config import supabase

class WatchlistDAO:
    def __init__(self):
        self.supabase = supabase
        self.table = "userwatchlist"

    # ---------------- Create ----------------
    def add_to_watchlist(self, user_id: str, movie_id: str, status: str = "planning", rating: int = None, review: str = None):
        """Insert a movie/show into a user's watchlist"""
        return self.supabase.table(self.table).insert({
            "user_id": user_id,
            "movie_id": movie_id,
            "status": status,
            "rating": rating,
            "review": review
        }).execute().data

    # ---------------- Read ----------------
    def get_watchlist_entry(self, watchlist_id: str):
        """Fetch a specific watchlist entry by its ID"""
        return self.supabase.table(self.table).select("*").eq("watchlist_id", watchlist_id).execute().data

    def get_user_watchlist(self, user_id: str):
        """Fetch the entire watchlist of a user"""
        return self.supabase.table(self.table).select("*").eq("user_id", user_id).execute().data

    def get_user_watchlist_by_status(self, user_id: str, status: str):
        """Fetch a user's watchlist filtered by status (watched, planning, dropped)"""
        return self.supabase.table(self.table).select("*").eq("user_id", user_id).eq("status", status).execute().data

    def get_user_watchlist_by_genre(self, user_id: str, genre_id: str):
        """
        Fetch a user's watchlist filtered by genre.
        NOTE: Requires a join between UserWatchlist, Movies_Shows, and MovieGenres.
        """
        query = self.supabase.rpc("get_user_watchlist_by_genre", {
            "uid": user_id,
            "gid": genre_id
        }).execute()
        return query.data

    # ---------------- Update ----------------
    def update_watchlist_entry(self, watchlist_id: str, status: str = None, rating: int = None, review: str = None):
        """Update watchlist entry details (status, rating, review)"""
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

    # ---------------- Delete ----------------
    def remove_from_watchlist(self, watchlist_id: str):
        """Delete a specific watchlist entry"""
        return self.supabase.table(self.table).delete().eq("watchlist_id", watchlist_id).execute().data


