from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Sample movie database
movies = {
    "Inception":     [1, 1, 0, 0],  # [Sci-fi, Thriller, Romance, Comedy]
    "Titanic":       [0, 0, 1, 0],
    "Interstellar":  [1, 1, 0, 0],
    "The Notebook":  [0, 0, 1, 0],
    "Superbad":      [0, 0, 0, 1],
    "Arrival":       [1, 1, 0, 0]
}

# User preference vector (likes Sci-fi and Thriller)
user_profile = np.array([1, 1, 0, 0])

# Calculate cosine similarity between user and each movie
def recommend_movies(user_vector, movie_db):
    recommendations = {}
    for title, features in movie_db.items():
        similarity = cosine_similarity([user_vector], [features])[0][0]
        recommendations[title] = similarity
    return sorted(recommendations.items(), key=lambda x: x[1], reverse=True)

# Get and print recommendations
recommended = recommend_movies(user_profile, movies)
print("Top Movie Recommendations:")
for title, score in recommended:
    print(f"{title} (Score: {score:.2f})")
