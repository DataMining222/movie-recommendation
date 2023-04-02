from src.models.Simple import build_chart
import requests
class SimpleControllers:
    def getSimple(genre):
        movies = build_chart(genre).to_dict('records')
        """[{
            "popularity": 34.457024,
            "title": "Dilwale Dulhania Le Jayenge",
            "vote_average": 9,
            "vote_count": 661,
            "wr": 8.463024318260317,
            "year": "1995"
        }, {},...]"""

        # loop through movies and call omdbapi for movie's poster image
        for movie in movies:
            movie_data = requests.get(f"https://www.omdbapi.com/?i={movie['imdb_id']}&apikey=810b65dc")
            movie_json = movie_data.json()
            movie['image'] = movie_json['Poster']

        res = {
            "data": movies
        }
        return res