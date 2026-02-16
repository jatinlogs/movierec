import axios from 'axios'
// helps in sending requests 

// base url
const API_BASE_URL = 'http://localhost:5000/api';

// searching movies by title
// this gets the query url 
export const searchMovies = async (query) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/search`, {
      params: { q: query, limit: 20 }
    });
    return response.data;
  } catch (error) {
    console.error('Error searching movies:', error);
    throw error;
  }
};


/**
 * Get movie recommendations
 */
export const getRecommendations = async (movieTitle, topN = 10) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/recommend`, {
      title: movieTitle,
      top_n: topN
    });
    return response.data;
  } catch (error) {
    console.error('Error getting recommendations:', error);
    throw error;
  }
};

/**
 * Health check
 */
export const healthCheck = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  } catch (error) {
    console.error('API health check failed:', error);
    throw error;
  }
};
