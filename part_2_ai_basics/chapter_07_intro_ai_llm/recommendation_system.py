# From: Zero to AI Agent, Chapter 7, Section 7.1
# File: recommendation_system.py

"""
A simplified recommendation system demonstrating how services like
Netflix, YouTube, and Spotify recommend content using AI patterns.
"""

import random
from collections import Counter

class SimpleRecommender:
    """
    Simulates how streaming services recommend content.
    This is a simplified version - real systems use:
    - Collaborative filtering (users who liked X also liked Y)
    - Content-based filtering (similar genres, actors, themes)
    - Deep learning for complex pattern recognition
    - Matrix factorization for finding hidden preferences
    """
    
    def __init__(self):
        self.user_history = []
        self.all_movies = {
            'action': ['Die Hard', 'Mad Max', 'John Wick', 'The Matrix', 'Mission Impossible'],
            'comedy': ['Airplane', 'Ghostbusters', 'The Hangover', 'Bridesmaids', 'Superbad'],
            'sci-fi': ['Interstellar', 'Arrival', 'Blade Runner', 'Dune', 'Ex Machina'],
            'drama': ['The Shawshank Redemption', 'Forrest Gump', 'The Godfather', 'Moonlight'],
            'horror': ['The Shining', 'Get Out', 'Hereditary', 'A Quiet Place', 'The Witch']
        }
        
        # In real systems, this would be learned from millions of users
        self.genre_relationships = {
            'action': ['sci-fi', 'thriller'],
            'sci-fi': ['action', 'thriller'],
            'comedy': ['romance', 'drama'],
            'drama': ['romance', 'thriller'],
            'horror': ['thriller', 'sci-fi']
        }
    
    def watch_movie(self, movie, genre, rating=None):
        """
        Records a movie watch event.
        Real systems track much more:
        - Time of day watched
        - How much was watched (did they finish?)
        - Device used
        - Whether they searched for it or clicked a recommendation
        """
        watch_data = {
            'movie': movie,
            'genre': genre,
            'rating': rating if rating else random.randint(3, 5)
        }
        self.user_history.append(watch_data)
        print(f"✅ You watched: {movie} ({genre}) - Rating: {watch_data['rating']}/5")
    
    def get_user_preferences(self):
        """
        Analyzes viewing history to understand preferences.
        Real systems use sophisticated algorithms to find patterns.
        """
        if not self.user_history:
            return None
        
        # Find favorite genres based on frequency and ratings
        genre_scores = {}
        for watch in self.user_history:
            genre = watch['genre']
            rating = watch['rating']
            
            if genre not in genre_scores:
                genre_scores[genre] = {'count': 0, 'total_rating': 0}
            
            genre_scores[genre]['count'] += 1
            genre_scores[genre]['total_rating'] += rating
        
        # Calculate weighted preferences
        preferences = {}
        for genre, scores in genre_scores.items():
            avg_rating = scores['total_rating'] / scores['count']
            # Weight by both frequency and rating
            preferences[genre] = scores['count'] * avg_rating
        
        return preferences
    
    def get_recommendations(self, num_recommendations=5):
        """
        Generates personalized recommendations.
        
        Real recommendation systems use:
        - Collaborative filtering: "Users like you also watched..."
        - Content similarity: "Because you liked The Matrix, try Inception"
        - Trending adjustments: Boost popular/new content
        - Diversity injection: Don't recommend all from same genre
        - Business rules: Promote originals, new releases
        """
        if not self.user_history:
            # Cold start problem - new users with no history
            print("🎬 New user detected! Here are popular picks:")
            popular_picks = []
            for genre, movies in self.all_movies.items():
                popular_picks.append(random.choice(movies))
            return popular_picks[:num_recommendations]
        
        # Get user preferences
        preferences = self.get_user_preferences()
        
        # Find top genres
        top_genres = sorted(preferences.items(), key=lambda x: x[1], reverse=True)
        if not top_genres:
            return []
        
        favorite_genre = top_genres[0][0]
        
        # Get unwatched movies from favorite genre
        watched = [watch['movie'] for watch in self.user_history]
        recommendations = []
        
        # Primary recommendations from favorite genre
        for movie in self.all_movies.get(favorite_genre, []):
            if movie not in watched:
                recommendations.append({
                    'movie': movie,
                    'reason': f"Because you love {favorite_genre} movies",
                    'confidence': 0.9
                })
        
        # Add related genre recommendations for diversity
        related_genres = self.genre_relationships.get(favorite_genre, [])
        for related_genre in related_genres:
            if related_genre in self.all_movies:
                for movie in self.all_movies[related_genre]:
                    if movie not in watched and len(recommendations) < num_recommendations * 2:
                        recommendations.append({
                            'movie': movie,
                            'reason': f"You might like {related_genre} (similar to {favorite_genre})",
                            'confidence': 0.7
                        })
        
        # Sort by confidence and return top N
        recommendations.sort(key=lambda x: x['confidence'], reverse=True)
        return recommendations[:num_recommendations]
    
    def explain_recommendations(self):
        """
        Shows how recommendations are generated.
        Transparency in AI systems helps build trust.
        """
        preferences = self.get_user_preferences()
        
        if not preferences:
            print("No viewing history yet!")
            return
        
        print("\n📊 YOUR VIEWING PROFILE:")
        print("-" * 40)
        
        total_watched = len(self.user_history)
        print(f"Movies watched: {total_watched}")
        
        # Show genre breakdown
        genre_counts = Counter(watch['genre'] for watch in self.user_history)
        print("\nGenre preferences:")
        for genre, count in genre_counts.most_common():
            percentage = (count / total_watched) * 100
            avg_rating = sum(w['rating'] for w in self.user_history if w['genre'] == genre) / count
            print(f"  • {genre}: {count} movies ({percentage:.0f}%) - Avg rating: {avg_rating:.1f}")
        
        print("\n🤖 HOW WE RECOMMEND:")
        print("-" * 40)
        print("1. Analyze your viewing history")
        print("2. Find your favorite genres")
        print("3. Consider your ratings")
        print("4. Look at related genres you might enjoy")
        print("5. Filter out what you've already seen")
        print("6. Rank by predicted enjoyment")


def demonstrate_recommendation_system():
    """Interactive demonstration of the recommendation system."""
    
    print("="*60)
    print("AI RECOMMENDATION SYSTEM DEMO")
    print("Like Netflix, YouTube, or Spotify")
    print("="*60)
    
    # Create recommender
    netflix_ai = SimpleRecommender()
    
    # Simulate viewing history
    print("\n📺 SIMULATING YOUR VIEWING HISTORY:")
    print("-" * 40)
    
    # User likes action movies
    netflix_ai.watch_movie('Die Hard', 'action', 5)
    netflix_ai.watch_movie('Mad Max', 'action', 4)
    netflix_ai.watch_movie('John Wick', 'action', 5)
    
    # Tried one comedy
    netflix_ai.watch_movie('Airplane', 'comedy', 3)
    
    # Loved a sci-fi movie
    netflix_ai.watch_movie('Interstellar', 'sci-fi', 5)
    
    # Explain the AI's understanding
    netflix_ai.explain_recommendations()
    
    # Get recommendations
    print("\n🎬 PERSONALIZED RECOMMENDATIONS FOR YOU:")
    print("-" * 40)
    recommendations = netflix_ai.get_recommendations()
    
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['movie']}")
        print(f"   Why: {rec['reason']}")
        print(f"   Confidence: {rec['confidence']*100:.0f}%")
    
    print("\n💡 REAL SYSTEMS ARE MORE COMPLEX:")
    print("-" * 40)
    print("• Track millions of users' behaviors")
    print("• Use deep neural networks")
    print("• Consider time of day, device, mood")
    print("• A/B test different algorithms")
    print("• Balance personalization with discovery")
    print("• Update in real-time as you watch")


if __name__ == "__main__":
    demonstrate_recommendation_system()
    
    print("\n" + "="*60)
    print("This is AI in your daily life!")
    print("Every 'For You' page uses similar patterns.")
    print("="*60)
