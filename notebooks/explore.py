import pandas as pd

# loading the dataset
try:
    print("Loading the Local dataset")
    df = pd.read_csv("data\TMDB_movie_dataset_v11.csv")

    print(f"Loaded data : {len(df)}")
    print(f"Columns in data : {len(df.columns)}")

except FileNotFoundError:
    print("----Could not found the CSV File----")
    exit()
except pd.errors.EmptyDataError:
    print("CSV file is Empty or no data")
    exit()
except Exception:
    print("Error Loading the Dataset")
    exit()

print("-"*30) # prints "-" 30 times
print("Columns in Data :- ")
print("-"*30)

for i,col in enumerate(df.columns,1):  # initial start index 1
    print(f"{i} -- {col}")

print("-"*30)

# Getting the first movie -------------------------------------
# first_movie = df.iloc[0] # item at location 0

# # Print the columns we care about
# print(f"Title: {first_movie['title']}")
# print(f"\nOverview: {first_movie['overview']}")
# print(f"\nGenres: {first_movie['genres']}")
# print(f"\nKeywords: {first_movie['keywords']}")
# print(f"\nTagline: {first_movie['tagline']}")
# print(f"\nRating: {first_movie['vote_average']}")
# print(f"Vote Count: {first_movie['vote_count']}")

# print("-"*30)

# Look at first 5 movies --------------------------------
# print("\n" + "="*60)
# print("FIRST 5 MOVIES:")
# print("="*60)

# for i in range(5):
#     movie = df.iloc[i]
#     print(f"\n{i+1}. {movie['title']} ({movie['vote_average']}⭐)")
#     print(f"   Genres: {movie['genres']}")
#     # Show just first 100 chars of overview
#     overview = str(movie['overview'])[:100]
#     print(f"   Overview: {overview}...")


# Check for missing values in important tags -----------------------
# print("\n" + "="*60)
# print("MISSING VALUES CHECK:")
# print("="*60)

# important_columns = ['title', 'overview', 'genres', 'keywords', 'tagline']

# for col in important_columns:
#     missing = df[col].isna().sum()
#     total = len(df)
#     percentage = (missing / total) * 100
#     print(f"{col:20s}: {missing:,} missing ({percentage:.2f}%)")


# data filtering - as in many of the movies - data is missing in tags -------------------------
print("-"*30)

print("Filtering for quality movies:-")
print("-"*30)

print(f"Length of Original data {len(df)}")

# Filter 1 - must have overview and genres
df_clean = df[df["overview"].notna() & df["genres"].notna()].copy() # copying notna df into df_clean
print(f"New data length after Filter 1 :- {len(df_clean)}")

# Filter 2 - Must be released
df_clean = df_clean[df_clean["status"] == "Released"].copy()
print(f"New data length after Filter 2 (must be released) :- {len(df_clean)}")

# Filter 3: Must have at least 10 votes (ensures it's a real, watched movie)
df_clean = df_clean[df_clean['vote_count'] >= 10].copy()
print(f"After keeping movies with ≥10 votes: {len(df_clean)}")

print("Final Cleaned Dataset")
print(f"reduced data from {len(df)} to {len(df_clean)}")


# creating tags column -------------------------------
print("-"*30)
print("Creating tags Column:-")
print("-"*30)

def create_tags(row): # combining all features into single column for every movie - in tags

    parts = [] # empty list we are going to start with

    # add overview if it exists in movie
    if pd.notna(row['overview']):
        parts.append(str(row['overview']))
    # Add genres
    if pd.notna(row['genres']):
        parts.append(str(row['genres']))
    
    # Add keywords
    if pd.notna(row['keywords']):
        parts.append(str(row['keywords']))
    
    # Add tagline
    if pd.notna(row['tagline']):
        parts.append(str(row['tagline']))
    
    # Combine all parts with spaces
    combined = ' '.join(parts)
    
    # convert to lowercase and remove extra spaces
    combined = combined.lower()
    combined = ' '.join(combined.split())  # removes extraspaces tags and new lines
    
    return combined

print("-"*30)
print("Creating tags for each movie")
print("-"*30)

df_clean['tags'] = df_clean.apply(create_tags, axis = 1) # axis 1 helps to run row by row - apply function on every row
print("Tags Created")
print("-"*30)

# checking tags
print("First Movie tag check --")
print(f"Title : {df_clean.iloc[0]['title']}")
print(f"Tags - {df_clean.iloc[0]['tags']}")
print("-"*30)
