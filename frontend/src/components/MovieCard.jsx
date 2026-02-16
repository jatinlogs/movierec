// src/components/MovieCard.jsx

import React from 'react';

const MovieCard = ({ movie, rank }) => {
  /**
   * Format similarity score as percentage
   */
  const formatSimilarity = (score) => {
    return `${(score * 100).toFixed(0)}%`;
  };

  return (
    <div className="movie-card">
      {/* Rank badge */}
      {rank && (
        <div className="rank-badge">
          #{rank}
        </div>
      )}

      {/* Movie poster placeholder */}
      <div className="movie-poster">
        🎬
      </div>

      {/* Movie info */}
      <div className="movie-info">
        <h3 className="movie-title">{movie.title}</h3>
        
        {/* Rating */}
        {movie.rating && (
          <div className="movie-rating">
            ⭐ {movie.rating.toFixed(1)}
          </div>
        )}

        {/* Similarity score */}
        {movie.similarity_score && (
          <div className="similarity-badge">
            Match: {formatSimilarity(movie.similarity_score)}
          </div>
        )}

        {/* Vote count */}
        {movie.vote_count && (
          <div className="movie-votes">
            {movie.vote_count.toLocaleString()} votes
          </div>
        )}
      </div>
    </div>
  );
};

export default MovieCard;