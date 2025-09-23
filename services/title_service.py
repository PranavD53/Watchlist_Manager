from dao.title_dao import TitleDAO

class TitleService:
    def __init__(self):
        self.dao = TitleDAO()

    def add_title(self, title: str, type_: str,genre =None):
        """Business rule: only allow valid types"""
        if type_.lower() not in ["movie", "show", "anime"]:
            return {"error": "Invalid type. Must be 'movie', 'show', or 'anime'."}
        return self.dao.add_title(title, type_.lower())

    def list_all_titles(self):
        """Fetch all titles"""
        return self.dao.list_titles()

    def search_titles(self, keyword: str):
        """Search titles by keyword"""
        return self.dao.search_titles(keyword)

    def update_title(self, movie_id: str, title: str = None, type_: str = None):
        """Update a movie/show/anime"""
        if type_ and type_.lower() not in ["movie", "show", "anime"]:
            return {"error": "Invalid type provided."}
        return self.dao.update_title(movie_id, title, type_)

    def delete_title(self, movie_id: str):
        """Delete a title"""
        return self.dao.delete_title(movie_id)
    
    def list_genres(self):
        return self.dao.list_genres()

    
    def search_movies(self, query):
        return self.dao.search_movies(query)