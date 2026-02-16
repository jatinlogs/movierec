// src/components/MovieSearch.jsx

import React, { useState, useEffect } from 'react';
import { searchMovies } from '../services/api';

const MovieSearch = ({ onMovieSelect }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);

  // Search when user types
  useEffect(() => {
    const search = async () => {
      if (searchTerm.length < 2) {
        setResults([]);
        setShowDropdown(false);
        return;
      }

      setIsLoading(true);
      try {
        const response = await searchMovies(searchTerm);
        if (response.success) {
          setResults(response.results);
          setShowDropdown(true);
        }
      } catch (error) {
        console.error('Search error:', error);
        setResults([]);
      } finally {
        setIsLoading(false);
      }
    };

    // Debounce search (wait 300ms after user stops typing)
    const timer = setTimeout(search, 300);
    return () => clearTimeout(timer);
  }, [searchTerm]);

  const handleSelect = (movie) => {
    setSearchTerm(movie.title);
    setShowDropdown(false);
    onMovieSelect(movie);
  };

  return (
    <div className="movie-search-container">
      <div className="search-input-wrapper">
        <input
          type="text"
          className="search-input"
          placeholder="🔍 Search for a movie... (e.g., Inception)"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onFocus={() => results.length > 0 && setShowDropdown(true)}
        />
        {isLoading && <div className="search-spinner">⟳</div>}
      </div>

      {showDropdown && results.length > 0 && (
        <div className="search-dropdown">
          {results.map((movie) => (
            <div
              key={movie.id}
              className="search-result-item"
              onClick={() => handleSelect(movie)}
            >
              <div className="result-title">{movie.title}</div>
              {movie.rating && (
                <div className="result-rating">⭐ {movie.rating.toFixed(1)}</div>
              )}
            </div>
          ))}
        </div>
      )}

      {showDropdown && results.length === 0 && searchTerm.length >= 2 && !isLoading && (
        <div className="search-dropdown">
          <div className="no-results">No movies found</div>
        </div>
      )}
    </div>
  );
};

export default MovieSearch;