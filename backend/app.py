from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd

# Initialize Flask app
app = Flask(__name__)
# CORS(app)  # Allow React to call our API
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

print("="*60)
print("LOADING RECOMMENDATION MODEL")
print("="*60)

# Load the model files
print("Loading models...")
try:
    with open('backend/models/similarity_matrix.pkl', 'rb') as f:
        similarity_matrix = pickle.load(f)
    print("✓ Similarity matrix loaded")
    
    with open('backend/models/movies_data.pkl', 'rb') as f:
        movies_df = pickle.load(f)
    print("✓ Movies data loaded")
    
    with open('backend/models/movie_list.pkl', 'rb') as f:
        movie_list = pickle.load(f)
    print("✓ Movie list loaded")
    
    print(f"\n✓ Model ready with {len(movies_df):,} movies!")
    
except Exception as e:
    print(f"❌ Error loading models: {e}")
    exit(1)

# endpoint 1 - testig route

@app.route('/api/health', methods=['GET'])
def health_check():
     return jsonify({
        'status': 'healthy',
        'total_movies': len(movies_df)
    })

# Endpoint 2  Get recommendations
@app.route('/api/recommend', methods=['POST'])
def recommend():
   
    try:
        # Get data from request
        data = request.get_json()
        
        # Validate input
        if not data or 'title' not in data:
            return jsonify({
                'success': False,
                'error': 'Movie title is required'
            }), 400
        
        movie_title = data['title']
        top_n = data.get('top_n', 10)  # Default to 10 if not provided
        
        # Find movie index
        matches = movies_df[movies_df['title'].str.lower() == movie_title.lower()]
        
        if len(matches) == 0:
            return jsonify({
                'success': False,
                'error': f'Movie "{movie_title}" not found in database'
            }), 404
        
        idx = matches.index[0]
        
        # Get similarity scores
        sim_scores = list(enumerate(similarity_matrix[idx]))
        
        # Sort by similarity (highest first)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top N (skip first - it's the movie itself)
        sim_scores = sim_scores[1:top_n+1]
        
        # Build recommendations list
        recommendations = []
        for movie_idx, score in sim_scores:
            movie = movies_df.iloc[movie_idx]
            
            rec = {
                'id': int(movie['id']),
                'title': movie['title'],
                'similarity_score': float(score),
                'rating': float(movie['vote_average']) if pd.notna(movie['vote_average']) else None,
                'vote_count': int(movie['vote_count']) if pd.notna(movie['vote_count']) else None
            }
            recommendations.append(rec)
        
        return jsonify({
            'success': True,
            'movie': movie_title,
            'count': len(recommendations),
            'recommendations': recommendations
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    
#endpoint 3 searching for the movies
@app.route('/api/search', methods = ['GET'])
def search():

    try:
        #getting query
        query = request.args.get('q','') # gets query from url , second params is default if not there
        limit = request.args.get('limit',10, type=int) # maximum return value 

        if not query or len(query) < 2:
            return jsonify({
                'success': False,
                'error': 'Search query must be at least 2 characters'
            }), 400
        
        # search case insenstivity
        query_lower = query.lower()
        
        matches = movies_df[movies_df['title'].str.lower().str.contains(query_lower, na=False)]
        
        # Limit results
        matches = matches.head(limit)
        
        # Format results
        results = []
        for _, movie in matches.iterrows():
            result = {
                'id': int(movie['id']),
                'title': movie['title'],
                'rating': float(movie['vote_average']) if pd.notna(movie['vote_average']) else None
            }
            results.append(result)
        
        return jsonify({
            'success': True,
            'query': query,
            'count': len(results),
            'results': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Run the app
if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0', port=5000)