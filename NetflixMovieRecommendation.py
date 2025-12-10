import React, { useState, useEffect } from 'react';
import { Play, ThumbsUp, ThumbsDown, Star, TrendingUp, Sparkles, X, Info } from 'lucide-react';

const NetflixRecommendationSystem = () => {
  const [userRatings, setUserRatings] = useState({});
  const [recommendations, setRecommendations] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [userProfile, setUserProfile] = useState(null);
  const [view, setView] = useState('browse');
  const [loading, setLoading] = useState(false);

  const movies = [
    { id: 1, title: "Inception", genre: ["Sci-Fi", "Thriller"], year: 2010, rating: 8.8, director: "Christopher Nolan", description: "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea.", tags: ["mind-bending", "action", "complex"], image: "🎬" },
    { id: 2, title: "The Shawshank Redemption", genre: ["Drama"], year: 1994, rating: 9.3, director: "Frank Darabont", description: "Two imprisoned men bond over years, finding solace and eventual redemption through acts of common decency.", tags: ["inspiring", "friendship", "classic"], image: "🎭" },
    { id: 3, title: "The Dark Knight", genre: ["Action", "Crime"], year: 2008, rating: 9.0, director: "Christopher Nolan", description: "Batman must accept one of the greatest psychological and physical tests to fight injustice.", tags: ["superhero", "dark", "action-packed"], image: "🦇" },
    { id: 4, title: "Pulp Fiction", genre: ["Crime", "Drama"], year: 1994, rating: 8.9, director: "Quentin Tarantino", description: "The lives of two mob hitmen, a boxer, and a pair of diner bandits intertwine in four tales of violence.", tags: ["nonlinear", "dialogue-heavy", "cult"], image: "🔫" },
    { id: 5, title: "Forrest Gump", genre: ["Drama", "Romance"], year: 1994, rating: 8.8, director: "Robert Zemeckis", description: "The presidencies of Kennedy and Johnson unfold through the perspective of an Alabama man.", tags: ["heartwarming", "inspirational", "historical"], image: "🏃" },
    { id: 6, title: "The Matrix", genre: ["Sci-Fi", "Action"], year: 1999, rating: 8.7, director: "Wachowski Brothers", description: "A computer hacker learns about the true nature of his reality and his role in the war against its controllers.", tags: ["philosophical", "action", "revolutionary"], image: "💊" },
    { id: 7, title: "Interstellar", genre: ["Sci-Fi", "Drama"], year: 2014, rating: 8.6, director: "Christopher Nolan", description: "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.", tags: ["space", "emotional", "complex"], image: "🚀" },
    { id: 8, title: "Goodfellas", genre: ["Crime", "Drama"], year: 1990, rating: 8.7, director: "Martin Scorsese", description: "The story of Henry Hill and his life in the mob, covering his relationship with his wife and his partners.", tags: ["biographical", "intense", "classic"], image: "🎰" },
    { id: 9, title: "The Silence of the Lambs", genre: ["Thriller", "Crime"], year: 1991, rating: 8.6, director: "Jonathan Demme", description: "A young FBI cadet must receive the help of an incarcerated cannibal killer to catch another serial killer.", tags: ["psychological", "suspenseful", "horror"], image: "🔪" },
    { id: 10, title: "Parasite", genre: ["Thriller", "Drama"], year: 2019, rating: 8.6, director: "Bong Joon-ho", description: "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.", tags: ["social-commentary", "twist", "foreign"], image: "🏠" },
    { id: 11, title: "Gladiator", genre: ["Action", "Drama"], year: 2000, rating: 8.5, director: "Ridley Scott", description: "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family.", tags: ["epic", "revenge", "historical"], image: "⚔️" },
    { id: 12, title: "The Prestige", genre: ["Mystery", "Thriller"], year: 2006, rating: 8.5, director: "Christopher Nolan", description: "After a tragic accident, two stage magicians engage in a battle to create the ultimate illusion.", tags: ["twist", "rivalry", "period"], image: "🎩" },
    { id: 13, title: "The Departed", genre: ["Crime", "Thriller"], year: 2006, rating: 8.5, director: "Martin Scorsese", description: "An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang.", tags: ["suspenseful", "complex", "gritty"], image: "👮" },
    { id: 14, title: "Whiplash", genre: ["Drama", "Music"], year: 2014, rating: 8.5, director: "Damien Chazelle", description: "A promising young drummer enrolls at a cut-throat music conservatory where his dreams hang in the balance.", tags: ["intense", "music", "psychological"], image: "🥁" },
    { id: 15, title: "The Lion King", genre: ["Animation", "Adventure"], year: 1994, rating: 8.5, director: "Roger Allers", description: "Lion prince Simba flees his kingdom after the murder of his father, only to learn the true meaning of responsibility.", tags: ["family", "classic", "animated"], image: "🦁" },
    { id: 16, title: "Spirited Away", genre: ["Animation", "Fantasy"], year: 2001, rating: 8.6, director: "Hayao Miyazaki", description: "During her family's move, a sullen 10-year-old girl wanders into a world ruled by gods and witches.", tags: ["magical", "coming-of-age", "anime"], image: "🏮" },
    { id: 17, title: "Joker", genre: ["Crime", "Drama"], year: 2019, rating: 8.4, director: "Todd Phillips", description: "In Gotham City, mentally troubled comedian Arthur Fleck embarks on a downward spiral of revolution and crime.", tags: ["dark", "character-study", "intense"], image: "🃏" },
    { id: 18, title: "Avengers: Endgame", genre: ["Action", "Adventure"], year: 2019, rating: 8.4, director: "Russo Brothers", description: "After Thanos's actions, the Avengers assemble once more to reverse the damage and restore balance to the universe.", tags: ["superhero", "epic", "blockbuster"], image: "💥" },
    { id: 19, title: "Coco", genre: ["Animation", "Adventure"], year: 2017, rating: 8.4, director: "Lee Unkrich", description: "A young boy accidentally enters the Land of the Dead and seeks the help of his musician great-great-grandfather.", tags: ["family", "music", "heartwarming"], image: "🎸" },
    { id: 20, title: "The Green Mile", genre: ["Drama", "Fantasy"], year: 1999, rating: 8.6, director: "Frank Darabont", description: "The lives of guards on Death Row are affected by one of their charges: a black man accused of murder.", tags: ["emotional", "supernatural", "powerful"], image: "⚡" }
  ];

  const calculateCosineSimilarity = (ratings1, ratings2) => {
    const commonMovies = Object.keys(ratings1).filter(id => ratings2[id]);
    if (commonMovies.length === 0) return 0;

    let dotProduct = 0;
    let norm1 = 0;
    let norm2 = 0;

    commonMovies.forEach(id => {
      dotProduct += ratings1[id] * ratings2[id];
      norm1 += ratings1[id] ** 2;
      norm2 += ratings2[id] ** 2;
    });

    return dotProduct / (Math.sqrt(norm1) * Math.sqrt(norm2));
  };

  const generateRecommendations = () => {
    setLoading(true);
    
    setTimeout(() => {
      const ratedMovieIds = Object.keys(userRatings).map(Number);
      const unratedMovies = movies.filter(m => !ratedMovieIds.includes(m.id));

      // Content-based filtering
      const ratedMovies = movies.filter(m => ratedMovieIds.includes(m.id));
      const userGenres = {};
      const userTags = {};
      
      ratedMovies.forEach(movie => {
        const rating = userRatings[movie.id];
        movie.genre.forEach(g => {
          userGenres[g] = (userGenres[g] || 0) + rating;
        });
        movie.tags.forEach(t => {
          userTags[t] = (userTags[t] || 0) + rating;
        });
      });

      // Calculate scores for unrated movies
      const scoredMovies = unratedMovies.map(movie => {
        let score = 0;
        
        // Genre match
        movie.genre.forEach(g => {
          score += (userGenres[g] || 0) * 2;
        });
        
        // Tag match
        movie.tags.forEach(t => {
          score += (userTags[t] || 0) * 1.5;
        });

        // Director match (if user liked other movies by same director)
        const directorMovies = ratedMovies.filter(m => m.director === movie.director);
        if (directorMovies.length > 0) {
          const avgDirectorRating = directorMovies.reduce((sum, m) => sum + userRatings[m.id], 0) / directorMovies.length;
          score += avgDirectorRating * 3;
        }

        // Boost highly rated movies
        score += movie.rating * 0.5;

        return { ...movie, recommendationScore: score };
      });

      // Sort and get top recommendations
      const topRecommendations = scoredMovies
        .sort((a, b) => b.recommendationScore - a.recommendationScore)
        .slice(0, 10);

      setRecommendations(topRecommendations);
      
      // Build user profile
      const topGenres = Object.entries(userGenres)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3)
        .map(([genre]) => genre);
      
      const topTags = Object.entries(userTags)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3)
        .map(([tag]) => tag);

      setUserProfile({
        totalRated: ratedMovieIds.length,
        avgRating: (Object.values(userRatings).reduce((a, b) => a + b, 0) / ratedMovieIds.length).toFixed(1),
        favoriteGenres: topGenres,
        favoriteTags: topTags
      });

      setLoading(false);
      setView('recommendations');
    }, 1500);
  };

  const rateMovie = (movieId, rating) => {
    setUserRatings(prev => ({
      ...prev,
      [movieId]: rating
    }));
  };

  const MovieCard = ({ movie, showRating = true }) => (
    <div className="bg-slate-900 rounded-lg overflow-hidden hover:scale-105 transition-transform duration-300 cursor-pointer">
      <div 
        className="h-48 bg-gradient-to-br from-red-900 to-slate-800 flex items-center justify-center text-6xl"
        onClick={() => setSelectedMovie(movie)}
      >
        {movie.image}
      </div>
      <div className="p-4">
        <h3 className="font-bold text-white mb-2 line-clamp-1">{movie.title}</h3>
        <div className="flex items-center gap-2 text-sm text-slate-400 mb-2">
          <Star className="w-4 h-4 text-yellow-400" fill="currentColor" />
          <span>{movie.rating}</span>
          <span>•</span>
          <span>{movie.year}</span>
        </div>
        <div className="flex flex-wrap gap-1 mb-3">
          {movie.genre.slice(0, 2).map(g => (
            <span key={g} className="text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded">
              {g}
            </span>
          ))}
        </div>
        {showRating && !userRatings[movie.id] && (
          <div className="flex gap-2">
            <button
              onClick={(e) => { e.stopPropagation(); rateMovie(movie.id, 5); }}
              className="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 rounded flex items-center justify-center gap-1"
            >
              <ThumbsUp className="w-4 h-4" />
            </button>
            <button
              onClick={(e) => { e.stopPropagation(); rateMovie(movie.id, 2); }}
              className="flex-1 bg-red-600 hover:bg-red-700 text-white py-2 rounded flex items-center justify-center gap-1"
            >
              <ThumbsDown className="w-4 h-4" />
            </button>
          </div>
        )}
        {showRating && userRatings[movie.id] && (
          <div className="bg-slate-800 text-center py-2 rounded text-green-400 font-semibold">
            Rated: {userRatings[movie.id]}/5 ⭐
          </div>
        )}
      </div>
    </div>
  );

  const MovieModal = ({ movie, onClose }) => (
    <div className="fixed inset-0 bg-black bg-opacity-90 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-slate-900 rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
        <div className="relative h-64 bg-gradient-to-br from-red-900 to-slate-800 flex items-center justify-center text-8xl">
          {movie.image}
          <button
            onClick={onClose}
            className="absolute top-4 right-4 bg-black bg-opacity-50 p-2 rounded-full hover:bg-opacity-70"
          >
            <X className="w-6 h-6 text-white" />
          </button>
        </div>
        <div className="p-6">
          <h2 className="text-3xl font-bold text-white mb-2">{movie.title}</h2>
          <div className="flex items-center gap-4 text-slate-400 mb-4">
            <div className="flex items-center gap-1">
              <Star className="w-5 h-5 text-yellow-400" fill="currentColor" />
              <span className="text-white font-semibold">{movie.rating}</span>
            </div>
            <span>•</span>
            <span>{movie.year}</span>
            <span>•</span>
            <span>{movie.director}</span>
          </div>
          <div className="flex flex-wrap gap-2 mb-4">
            {movie.genre.map(g => (
              <span key={g} className="bg-slate-800 text-slate-300 px-3 py-1 rounded-full">
                {g}
              </span>
            ))}
          </div>
          <p className="text-slate-300 mb-4 leading-relaxed">{movie.description}</p>
          <div className="flex flex-wrap gap-2 mb-6">
            {movie.tags.map(t => (
              <span key={t} className="text-xs bg-slate-800 text-slate-400 px-2 py-1 rounded">
                #{t}
              </span>
            ))}
          </div>
          {!userRatings[movie.id] ? (
            <div className="flex gap-3">
              <button
                onClick={() => { rateMovie(movie.id, 5); onClose(); }}
                className="flex-1 bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg flex items-center justify-center gap-2 font-semibold"
              >
                <ThumbsUp className="w-5 h-5" />
                I Like This
              </button>
              <button
                onClick={() => { rateMovie(movie.id, 2); onClose(); }}
                className="flex-1 bg-red-600 hover:bg-red-700 text-white py-3 rounded-lg flex items-center justify-center gap-2 font-semibold"
              >
                <ThumbsDown className="w-5 h-5" />
                Not For Me
              </button>
            </div>
          ) : (
            <div className="bg-slate-800 text-center py-4 rounded-lg">
              <span className="text-green-400 font-semibold text-lg">
                ✓ You rated this {userRatings[movie.id]}/5 stars
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <div className="bg-gradient-to-b from-red-900 to-black py-6 px-6 sticky top-0 z-40 backdrop-blur-sm bg-opacity-90">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="text-4xl font-bold text-red-600">N</div>
            <h1 className="text-2xl font-bold">AI Recommendations</h1>
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={() => setView('browse')}
              className={`px-4 py-2 rounded ${view === 'browse' ? 'bg-red-600' : 'bg-slate-800 hover:bg-slate-700'}`}
            >
              Browse
            </button>
            <button
              onClick={() => view === 'browse' && Object.keys(userRatings).length >= 3 && generateRecommendations()}
              disabled={Object.keys(userRatings).length < 3}
              className={`px-4 py-2 rounded flex items-center gap-2 ${
                Object.keys(userRatings).length >= 3 
                  ? 'bg-green-600 hover:bg-green-700' 
                  : 'bg-slate-700 cursor-not-allowed opacity-50'
              }`}
            >
              <Sparkles className="w-4 h-4" />
              Get AI Recommendations
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {view === 'browse' && (
          <>
            {/* Stats Bar */}
            <div className="bg-slate-900 rounded-lg p-6 mb-8">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-semibold mb-2">Rate Movies to Get Started</h2>
                  <p className="text-slate-400">
                    Rate at least 3 movies to get personalized AI recommendations
                  </p>
                </div>
                <div className="text-center">
                  <div className="text-4xl font-bold text-red-600">{Object.keys(userRatings).length}</div>
                  <div className="text-slate-400">Movies Rated</div>
                </div>
              </div>
              {Object.keys(userRatings).length >= 3 && (
                <div className="mt-4 p-4 bg-green-900 bg-opacity-30 border border-green-600 rounded-lg flex items-center gap-3">
                  <TrendingUp className="w-6 h-6 text-green-400" />
                  <span className="text-green-400">Ready! Click "Get AI Recommendations" to see your personalized picks</span>
                </div>
              )}
            </div>

            {/* Movie Grid */}
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
              {movies.map(movie => (
                <MovieCard key={movie.id} movie={movie} />
              ))}
            </div>
          </>
        )}

        {view === 'recommendations' && !loading && (
          <>
            {/* User Profile */}
            {userProfile && (
              <div className="bg-gradient-to-r from-red-900 to-purple-900 rounded-lg p-6 mb-8">
                <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                  <Sparkles className="w-6 h-6" />
                  Your Taste Profile
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div className="bg-black bg-opacity-30 rounded-lg p-4">
                    <div className="text-3xl font-bold">{userProfile.totalRated}</div>
                    <div className="text-slate-300">Movies Rated</div>
                  </div>
                  <div className="bg-black bg-opacity-30 rounded-lg p-4">
                    <div className="text-3xl font-bold">{userProfile.avgRating}⭐</div>
                    <div className="text-slate-300">Avg Rating</div>
                  </div>
                  <div className="bg-black bg-opacity-30 rounded-lg p-4">
                    <div className="text-sm font-semibold mb-2">Favorite Genres</div>
                    <div className="flex flex-wrap gap-1">
                      {userProfile.favoriteGenres.map(g => (
                        <span key={g} className="text-xs bg-red-600 px-2 py-1 rounded">{g}</span>
                      ))}
                    </div>
                  </div>
                  <div className="bg-black bg-opacity-30 rounded-lg p-4">
                    <div className="text-sm font-semibold mb-2">Your Preferences</div>
                    <div className="flex flex-wrap gap-1">
                      {userProfile.favoriteTags.map(t => (
                        <span key={t} className="text-xs bg-purple-600 px-2 py-1 rounded">#{t}</span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Recommendations */}
            <div className="mb-8">
              <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                <TrendingUp className="w-6 h-6 text-green-400" />
                Recommended For You
              </h2>
              <p className="text-slate-400 mb-6">
                Based on your ratings, our AI recommends these movies tailored to your taste
              </p>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
                {recommendations.map(movie => (
                  <MovieCard key={movie.id} movie={movie} showRating={false} />
                ))}
              </div>
            </div>

            {/* Discovery Section */}
            <div className="bg-slate-900 rounded-lg p-6">
              <h3 className="text-xl font-bold mb-4">Want Better Recommendations?</h3>
              <p className="text-slate-400 mb-4">Rate more movies to improve your recommendations!</p>
              <button
                onClick={() => setView('browse')}
                className="bg-red-600 hover:bg-red-700 px-6 py-3 rounded-lg font-semibold"
              >
                Rate More Movies
              </button>
            </div>
          </>
        )}

        {loading && (
          <div className="text-center py-20">
            <div className="inline-block animate-spin rounded-full h-16 w-16 border-t-4 border-red-600 mb-4"></div>
            <h3 className="text-2xl font-bold mb-2">AI is Analyzing Your Preferences...</h3>
            <p className="text-slate-400">Building your personalized recommendation profile</p>
          </div>
        )}
      </div>

      {/* Movie Detail Modal */}
      {selectedMovie && (
        <MovieModal movie={selectedMovie} onClose={() => setSelectedMovie(null)} />
      )}
    </div>
  );
};

export default NetflixRecommendationSystem;
