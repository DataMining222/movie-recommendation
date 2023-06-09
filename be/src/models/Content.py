import pandas as pd
import numpy as np
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from fuzzywuzzy import fuzz


import warnings; warnings.simplefilter('ignore')

credits = pd.read_csv('./input_data/movie_dataset/credits.csv')
keywords = pd.read_csv('./input_data/movie_dataset/keywords.csv')
links_small = pd.read_csv('./input_data/movie_dataset/links_small.csv')
md = pd.read_csv('./input_data/movie_dataset/movies_metadata.csv')
ratings = pd.read_csv('./input_data/movie_dataset/ratings_small.csv')

vote_counts = md[md['vote_count'].notnull()]['vote_count'].astype('int')

# this is R
vote_averages = md[md['vote_average'].notnull()]['vote_average'].astype('int')

# this is C
C = vote_averages.mean()

m = vote_counts.quantile(0.95)

def weighted_rating(x):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+m) * R) + (m/(m+v) * C)

def convert_int(x):
    try:
        return int(x)
    except:
        return np.nan
    
def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

def filter_keywords(x):
    words = []
    for i in x:
        if i in s:
            words.append(i)
    return words

links_small = links_small[links_small['tmdbId'].notnull()]['tmdbId'].astype('int')

md['genres'] = md['genres'].fillna('[]').apply(literal_eval).apply(lambda x: [i[
    'name'] for i in x] if isinstance(x, list) else [])

md['year'] = pd.to_datetime(md['release_date'], errors='coerce').apply(
    lambda x: str(x).split('-')[0] if x != np.nan else np.nan)

    
md['id'] = md['id'].apply(convert_int)
md = md.drop([19730, 29503, 35587])
md['id'] = md['id'].astype('int')

smd = md[md['id'].isin(links_small)]
smd['tagline'] = smd['tagline'].fillna('')
smd['description'] = smd['overview'] + smd['tagline']
smd['description'] = smd['description'].fillna('')

smd = smd.reset_index()
titles = smd['title']
indices = pd.Series(smd.index, index=smd['title'])
# Test

keywords['id'] = keywords['id'].astype('int')
credits['id'] = credits['id'].astype('int')
md['id'] = md['id'].astype('int')

md = md.merge(credits, on='id')
md = md.merge(keywords, on='id')

smd = md[md['id'].isin(links_small)]

smd['cast'] = smd['cast'].apply(literal_eval)
smd['crew'] = smd['crew'].apply(literal_eval)
smd['keywords'] = smd['keywords'].apply(literal_eval)
smd['cast_size'] = smd['cast'].apply(lambda x: len(x))
smd['crew_size'] = smd['crew'].apply(lambda x: len(x))

smd['director'] = smd['crew'].apply(get_director)
smd['cast'] = smd['cast'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
smd['cast'] = smd['cast'].apply(lambda x: x[:3] if len(x) >=3 else x)
smd['keywords'] = smd['keywords'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

smd['cast'] = smd['cast'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])
smd['director'] = smd['director'].astype('str').apply(lambda x: str.lower(x.replace(" ", "")))
smd['director'] = smd['director'].apply(lambda x: [x,x, x])

s = smd.apply(lambda x: pd.Series(x['keywords']),axis=1).stack().reset_index(level=1, drop=True)
s.name = 'keyword'
s = s.value_counts()

s = s[s > 1]
stemmer = SnowballStemmer('english')
stemmer.stem('dogs')

smd['keywords'] = smd['keywords'].apply(filter_keywords)
smd['keywords'] = smd['keywords'].apply(lambda x: [stemmer.stem(i) for i in x])
smd['keywords'] = smd['keywords'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])

smd['soup'] = smd['keywords'] + smd['cast'] + smd['director'] + smd['genres']
smd['soup'] = smd['soup'].apply(lambda x: ' '.join(x))

count = CountVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
count_matrix = count.fit_transform(smd['soup'])

cosine_sim = cosine_similarity(count_matrix, count_matrix)

smd = smd.reset_index()
titles = smd['title']
indices = pd.Series(smd.index, index=smd['title'])

# def get_recommendations(title):
#     idx = indices[title]
#     sim_scores = list(enumerate(cosine_sim[idx]))
#     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#     sim_scores = sim_scores[1:26]
#     movie_indices = [i[0] for i in sim_scores]
    
#     movies = smd.iloc[movie_indices][['imdb_id','title', 'vote_count', 'vote_average', 'year']]
#     vote_counts = movies[movies['vote_count'].notnull()]['vote_count'].astype('int')
#     vote_averages = movies[movies['vote_average'].notnull()]['vote_average'].astype('int')
#     C = vote_averages.mean()
#     m = vote_counts.quantile(0.60)
#     qualified = movies[(movies['vote_count'] >= m) & (movies['vote_count'].notnull()) & 
#                        (movies['vote_average'].notnull())]
#     qualified['vote_count'] = qualified['vote_count'].astype('int')
#     qualified['vote_average'] = qualified['vote_average'].astype('int')
#     qualified['wr'] = qualified.apply(weighted_rating, axis=1)
#     qualified = qualified.sort_values('wr', ascending=False).head(10)
#     return qualified

from fuzzywuzzy import fuzz

def get_recommendations(title):
    # Convert input title to lowercase
    title_lower = title.lower()

    # Find closest matching title in smd DataFrame
    closest_match = None
    closest_match_ratio = -1
    for smd_title in smd['title'].values:
        # Compare lowercase versions of titles using fuzzy string matching
        ratio = fuzz.ratio(title_lower, smd_title.lower())
        if ratio > closest_match_ratio:
            closest_match = smd_title
            closest_match_ratio = ratio

    # Check if closest match meets a minimum similarity threshold
    if closest_match_ratio < 50:
        return "No matches found. Please try again with a different title."

    # Get indices of top 25 most similar movies
    idx = indices[closest_match]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    movie_indices = [i[0] for i in sim_scores]

    # Filter and sort qualified movies by weighted rating
    qualified = smd.iloc[movie_indices][['imdb_id', 'title', 'vote_count', 'vote_average', 'year']]
    vote_counts = qualified[qualified['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = qualified[qualified['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(0.60)
    qualified = qualified[(qualified['vote_count'] >= m) & (qualified['vote_count'].notnull()) & 
                       (qualified['vote_average'].notnull())]
    qualified['vote_count'] = qualified['vote_count'].astype('int')
    qualified['vote_average'] = qualified['vote_average'].astype('int')
    qualified['wr'] = qualified.apply(weighted_rating, axis=1)
    qualified = qualified.sort_values('wr', ascending=False).head(10)
    return qualified