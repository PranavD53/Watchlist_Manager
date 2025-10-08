from dao.title_dao import TitleDAO

class TitleService:
    def __init__(self):
        self.dao = TitleDAO()

    def add_title(self, title: str, type_: str,genre =None):
        if type_.lower() not in ["movie", "show", "anime"]:
            return {"error": "Invalid type. Must be 'Movie', 'Show', or 'Anime'."}
        return self.dao.add_title(title, type_.lower())

    def list_all_titles(self):
        return self.dao.list_titles()

    def search_titles(self, keyword: str):
        return self.dao.search_titles(keyword)

    def delete_title(self, movie_id: str):
        return self.dao.delete_title(movie_id)
    
    def list_genres(self):
        return self.dao.list_genres()

    def search_movies(self, query):
        return self.dao.search_movies(query)
    
    def update_title(self, movie_id: str, title: str = None, type_: str = None, genre: str = None):
        if type_ and type_.lower() not in ["Movie", "Show", "Anime"]:
            return {"error": "Invalid type provided."}
        return self.dao.update_title(movie_id, title, type_, genre)
    
    def get_title(self,movie_id):
        return self.dao.get_title_by_id(movie_id)