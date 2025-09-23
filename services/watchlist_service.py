from dao.watchlist_dao import WatchlistDAO
from dao.title_dao import TitleDAO
from dao.user_dao import UserDAO

class WatchlistService:
    def __init__(self):
        self.dao = WatchlistDAO()
        self.user_dao = UserDAO()
        self.title_dao = TitleDAO()

    # ---- Watchlist Operations ----
    def add_to_watchlist(self, user_id: str, movie_id: str, status: str = "planning", rating: int = None, review: str = None):
        """Business rules:
        - User must exist 
        - Title must exist 
        - Status must be valid
        """
        user = self.user_dao.get_user_by_id(user_id)
        if not user:
            return {"error": "User not found."}

        movie = self.title_dao.get_title_by_id(movie_id)
        if not movie:
            return {"error": "Movie/Show not found."}

        if status.lower() not in ["watched", "planning", "dropped"]:
            return {"error": "Invalid status. Use: watched, planning, or dropped."}

        return self.dao.add_to_watchlist(user_id, movie_id, status.lower(), rating, review)

    def get_user_watchlist(self, user_id: str):
        """Get full watchlist for a user"""
        return self.dao.get_user_watchlist(user_id)

    def get_user_watchlist_by_status(self, user_id: str, status: str):
        """Filter watchlist by status"""
        if status.lower() not in ["watched", "planning", "dropped"]:
            return {"error": "Invalid status filter."}
        return self.dao.get_user_watchlist_by_status(user_id, status.lower())

    def update_watchlist_entry(self, watchlist_id: str, status: str = None, rating: int = None, review: str = None):
        """Update a watchlist entry"""
        if status and status.lower() not in ["watched", "planning", "dropped"]:
            return {"error": "Invalid status."}
        return self.dao.update_watchlist_entry(watchlist_id, status, rating, review)

    def remove_from_watchlist(self, watchlist_id: str):
        """Delete a watchlist entry"""
        return self.dao.remove_from_watchlist(watchlist_id)

