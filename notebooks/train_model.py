import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("-"*15)
print("Building Model")
print("-"*15)

# Loading the dataset
print("Loading dataset:-")
df = pd.read_csv("data\movies_cleaned.csv")
print(f"Loaded CSV : {len(df)} , data extracted")

# NEW: Sort by popularity and keep top movies ( helps to tackle with memory error if we use all the movies - cosine similarity comapres with every memory ram will expload)
print("\nFiltering to top movies by vote count...")
df = df.sort_values('vote_count', ascending=False).head(10000).copy()
df = df.reset_index(drop=True)
print(f"Kept top {len(df):,} most popular movies")

# checking tags that is must required (in case if not there)
if df['tags'].isna().sum() > 0:
    print(f"Warning - tags are missing - {df['tags'].isna().sum()} : found missing")
    # cleaning again
    df = df[df['tags'].notna()].copy()
    print(f"New cleaned dataset - {len(df)}, new count")

#_____________________________________________
# creating TFIDF Vectors

print("Creating TF IDF Vectors")

tfidf = TfidfVectorizer(
    max_features = 5000, # keeps max words to 5000
    stop_words = "english", # removes the common english words
    lowercase = True # in case if not lowercase although we have done that
)

tfidf_matrix = tfidf.fit_transform(df['tags'])

print("Created TFIDF Matrix")
print(f"shape of matrix : {tfidf_matrix.shape}")

# now next cosine similarity
print("Calculating Cosine Similarity")

similarity_matrix = cosine_similarity(tfidf_matrix,tfidf_matrix) # comapares every movie with every other

print(similarity_matrix.shape)

# creating reccomendation functions

def get_recommendations(movie_title, top_n = 10):
    
    #finding Movie index that is entered
    try:
        idx = df[df['title'].str.lower() == movie_title.lower()].index[0] # index 0 gives us the first column of the movie where and on which index movie is located
    except IndexError:
        return f"Movie {movie_title} Not found"
    
    # getting similarity scores of the movie we just extracted the index of
    sim_scores = list(enumerate(similarity_matrix[idx]))

    # sorting the simiaraty scores in desending
    sim_scores = sorted(sim_scores, key= lambda x : x[1], reverse=True)

    # get top N recc.
    sim_scores = sim_scores[1:top_n + 1] # we excluded 0 as it is movie itself

    #getting movie indexes of the movies sorted
    movie_indexes = [i[0] for i in sim_scores] # gives the indexes

    #returing movie titles
    recommendations = df.iloc[movie_indexes][['title','vote_count']].copy()
    recommendations['similarity'] = [score[1] for score in sim_scores] # returns index 1 in sim scores and add into recc.

    return recommendations

# # testing recc. functions
# print("testing recc. function")
# recs = get_recommendations("inception",5)
# print(recs.to_string(index = False))

# Testing 
print("\n" + "="*60)
print("TESTING WITH DIFFERENT MOVIES:")
print("="*60)

test_movies = ['The Dark Knight', 'Toy Story', 'The Matrix']
for movie in test_movies:
    print(f"\nRecommendations for '{movie}':")
    recs = get_recommendations(movie, top_n=3)
    if isinstance(recs, str):
        print(f"  {recs}")
    else:
        for _, row in recs.iterrows():
            print(f"  • {row['title']} (similarity: {row['similarity']:.3f})")

# saving Model
print("Saving model and data...")

import os
os.makedirs('backend\models', exist_ok=True)

# Save similarity matrix
print("  Saving similarity matrix...")
with open('backend\models\similarity_matrix.pkl', 'wb') as f:
    pickle.dump(similarity_matrix, f)
print("similarity_matrix.pkl saved")

# Save movie dataframe
print("  Saving movie data...")
with open('backend\models\movies_data.pkl', 'wb') as f:
    pickle.dump(df, f)
print("movies_data.pkl saved")

# Save just movie titles for the frontend
print("  Saving movie list...")
movie_list = df[['id', 'title']].to_dict('records')
with open('backend\models\movie_list.pkl', 'wb') as f:
    pickle.dump(movie_list, f)
print("movie_list.pkl saved")

print("-"*30)
print("Model Training Complete")
print("-"*30)
