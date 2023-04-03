from src.models.Hybrid import get_recommendations
import requests
class HybridControllers:
    def getHybrid(title):
        movies = get_recommendations(1, title).to_dict('records')

        for movie in movies:
            movie_data = requests.get(f"https://www.omdbapi.com/?i={movie['imdb_id']}&apikey=810b65dc")
            movie_json = movie_data.json()
            movie['image'] = movie_json['Poster']

        res = {
            "Search": movies
        }
        return res
    