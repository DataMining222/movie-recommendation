from src.models.Content import get_recommendations
import requests
class ContentControllers:
    def getContent(title):
        movies = get_recommendations(title).to_dict('records')

        for movie in movies:
            movie_data = requests.get(f"https://www.omdbapi.com/?i={movie['imdb_id']}&apikey=f31303c2")
            movie_json = movie_data.json()
            movie['image'] = movie_json['Poster']

        res = {
            "Search": movies
        }
        return res
    