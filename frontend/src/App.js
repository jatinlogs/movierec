// src/App.js

import React, { useState, useEffect } from 'react';
import MovieSearch from './components/MovieSearch';
import MovieCard from './components/MovieCard';
import { getRecommendations, healthCheck } from './services/api';
import './App.css';

function App() {
  // State management
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [apiStatus, setApiStatus] = useState('checking');

  /**
   * Check if Flask API is running (runs once on page load)
   */
  useEffect(() => {
    const checkAPI = async () => {
      try {
        await healthCheck();
        setApiStatus('connected');
      } catch (error) {
        setApiStatus('disconnected');
      }
    };
    checkAPI();
  }, []);

  /**
   * Handle movie selection from search
   */
  const handleMovieSelect = async (movie) => {
    setSelectedMovie(movie);
    setError(null);
    setIsLoading(true);
    setRecommendations([]);

    try {
      const response = await getRecommendations(movie.title, 10);

      if (response.success) {
        setRecommendations(response.recommendations);
      } else {
        setError(response.error);
      }
    } catch (err) {
      setError('Failed to connect to server. Make sure Flask is running!');
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Reset to initial state
   */
  const handleReset = () => {
    setSelectedMovie(null);
    setRecommendations([]);
    setError(null);
  };

  return (
    <div className="App">
      {/* Header */}
      <header className="app-header">
        <h1>MovieRec</h1>
        <p>Find movies you'll love using AI</p>
        
        {/* API Status */}
        <div className={`api-status ${apiStatus}`}>
          {apiStatus === 'connected' && '✓ API Connected'}
          {apiStatus === 'disconnected' && '✗ API Offline'}
          {apiStatus === 'checking' && '⟳ Checking...'}
        </div>
      </header>

      {/* Main Content */}
      <main className="app-main">
        
        {/* Search Section */}
        <section className="search-section">
          <MovieSearch onMovieSelect={handleMovieSelect} />
          
          {selectedMovie && (
            <div className="selected-movie">
              <p>Getting recommendations for:</p>
              <h2>{selectedMovie.title}</h2>
              <button onClick={handleReset} className="reset-btn">
                Try Another Movie
              </button>
            </div>
          )}
        </section>

        {/* Loading State */}
        {isLoading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Finding similar movies...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="error">
            <h3>❌ Oops!</h3>
            <p>{error}</p>
            <button onClick={handleReset}>Try Again</button>
          </div>
        )}

        {/* Recommendations */}
        {/* Recommendations - Netflix Style Carousel */}
        {!isLoading && !error && recommendations.length > 0 && (
          <section className="recommendations">
            <h2>🎬 Recommended For You</h2>
            <p className="rec-count">
              {recommendations.length} movies perfectly matched
            </p>
            
            <div className="movie-carousel">
              <div className="carousel-track" id="carousel-track">
                {recommendations.map((movie, index) => (
                  <MovieCard 
                    key={movie.id} 
                    movie={movie} 
                    rank={index + 1} 
                  />
                ))}
              </div>
              
              <div className="carousel-buttons">
                <button 
                  className="carousel-btn left"
                  onClick={() => {
                    document.getElementById('carousel-track').scrollBy({
                      left: -350,
                      behavior: 'smooth'
                    });
                  }}
                >
                  ‹
                </button>
                <button 
                  className="carousel-btn right"
                  onClick={() => {
                    document.getElementById('carousel-track').scrollBy({
                      left: 350,
                      behavior: 'smooth'
                    });
                  }}
                >
                  ›
                </button>
              </div>
            </div>
          </section>
        )}

        {/* Empty State */}
        {!isLoading && !error && !selectedMovie && (
          <div className="empty-state">
            <h2>👋 Heyaa!</h2>
            <p>Search for a movie above to get AI-powered recommendations</p>
            <div className="features">
              <div className="feature">Machine Learning Powered</div>
              <div className="feature">Personalized Results</div>
              <div className="feature">Instant Recommendations</div>
            </div>
          </div>
        )}

      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>Built with React, Flask & Machine Learning</p>
      </footer>
    </div>
  );
}

export default App;