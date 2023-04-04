# import matplotlib.pyplot as plt
# from src.models.Simple import weighted_rating
# import seaborn as sns
# import pandas as pd
# import numpy as np
# import ast 
# from scipy import stats
# from ast import literal_eval
# from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
# from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
# from nltk.stem.snowball import SnowballStemmer
# from nltk.stem.wordnet import WordNetLemmatizer
# from nltk.corpus import wordnet
# from surprise.model_selection import cross_validate
# from surprise import Reader, Dataset, SVD

# import warnings; warnings.simplefilter('ignore')

# credits = pd.read_csv('./input_data/movie_dataset/credits.csv')
# keywords = pd.read_csv('./input_data/movie_dataset/keywords.csv')
# links_small = pd.read_csv('./input_data/movie_dataset/links_small.csv')
# md = pd.read_csv('./input_data/movie_dataset/movies_metadata.csv')
# ratings = pd.read_csv('./input_data/movie_dataset/ratings_small.csv')

# reader = Reader()

# data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
# svd = SVD()
# cross_validate(svd, data, measures=['RMSE'], cv=5)

# trainset = data.build_full_trainset()
# svd.fit(trainset)

# ratings[ratings['userId'] == 1]