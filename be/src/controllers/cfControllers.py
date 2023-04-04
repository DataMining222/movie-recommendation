# from src.models.CF import get_recommendations
# import requests
# class CFControllers:
#     def getCF(title):
#         print(title)
#         movies = get_recommendations(title).to_dict('records')

#         for movie in movies:
#             movie_data = requests.get(f"https://www.omdbapi.com/?i={movie['imdb_id']}&apikey=810b65dc")
#             movie_json = movie_data.json()
#             movie['image'] = movie_json['Poster']

#         res = {
#             "data": movies
#         }
#         return res