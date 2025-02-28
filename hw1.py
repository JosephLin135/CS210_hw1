# FILL IN ALL THE FUNCTIONS IN THIS TEMPLATE
# MAKE SURE YOU TEST YOUR FUNCTIONS WITH MULTIPLE TEST CASES
# ASIDE FROM THE SAMPLE FILES PROVIDED TO YOU, TEST ON YOUR OWN FILES

# WHEN DONE, SUBMIT THIS FILE TO AUTOLAB

from collections import defaultdict
from collections import Counter

# YOU MAY NOT CODE ANY OTHER IMPORTS

# ------ TASK 1: READING DATA  --------


# 1.1
def read_ratings_data(f):
    # parameter f: movie ratings file name f (e.g. "movieRatingSample.txt")
    # return: dictionary that maps movie to ratings
    # WRITE YOUR CODE BELOW

    ratings_data = defaultdict(list)

    with open(f, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split("|")
                if len(parts) == 3:
                    movie, rating, _ = map(str.strip, parts)
                    ratings_data.setdefault(movie, []).append(float(rating))

    return ratings_data


# 1.2
def read_movie_genre(f):
    # parameter f: movies genre file name f (e.g. "genreMovieSample.txt")
    # return: dictionary that maps movie to genre
    # WRITE YOUR CODE BELOW

    movie_genres = {}

    with open(f, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split("|")

                if len(parts) == 3:
                    genre, _, movie = map(str.strip, parts)
                    movie_genres[movie] = genre

    return movie_genres


# ------ TASK 2: PROCESSING DATA --------


# 2.1
def create_genre_dict(d):
    # parameter d: dictionary that maps movie to genre
    # return: dictionary that maps genre to movies
    # WRITE YOUR CODE BELOW

    genre_dict = defaultdict(list)
    for movie, genre in d.items():
        if genre not in genre_dict:
            genre_dict[genre] = []
        genre_dict[genre].append(movie)

    return genre_dict


# 2.2
def calculate_average_rating(d):
    # parameter d: dictionary that maps movie to ratings
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW

    average_ratings = {}
    for movie, ratings in d.items():
        if ratings:
            average_ratings[movie] = sum(ratings) / len(ratings)

    return average_ratings


# ------ TASK 3: RECOMMENDATION --------


# 3.1
def get_popular_movies(d, n=10):
    # parameter d: dictionary that maps movie to average rating
    # parameter n: integer (for top n), default value 10
    # return: dictionary that maps movie to average rating,
    #         in ranked order from highest to lowest average rating
    # WRITE YOUR CODE BELOW

    sorted_movies = sorted(d.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_movies[:n])


# 3.2
def filter_movies(d, thres_rating=3):
    # parameter d: dictionary that maps movie to average rating
    # parameter thres_rating: threshold rating, default value 3
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW

    return {movie: rating for movie, rating in d.items() if rating >= thres_rating}


# 3.3
def get_popular_in_genre(genre, genre_to_movies, movie_to_average_rating, n=5):
    # parameter genre: genre name (e.g. "Comedy")
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # parameter n: integer (for top n), default value 5
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW

    movies_in_genre = genre_to_movies.get(genre, [])
    genre_ratings = {movie: movie_to_average_rating[movie] for movie in movies_in_genre}
    sorted_movies = sorted(genre_ratings.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_movies[:n])


# 3.4
def get_genre_rating(genre, genre_to_movies, movie_to_average_rating):
    # parameter genre: genre name (e.g. "Comedy")
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # return: average rating of movies in genre
    # WRITE YOUR CODE BELOW

    movies_in_genre = genre_to_movies.get(genre, [])
    if not movies_in_genre:
        return 0
    total_rating = sum(movie_to_average_rating[movie] for movie in movies_in_genre)
    return total_rating / len(movies_in_genre)


# 3.5
def genre_popularity(genre_to_movies, movie_to_average_rating, n=5):
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # parameter n: integer (for top n), default value 5
    # return: dictionary that maps genre to average rating
    # WRITE YOUR CODE BELOW

    genre_avg_ratings = {}
    for genre, movies in genre_to_movies.items():
        genre_avg_ratings[genre] = get_genre_rating(
            genre, genre_to_movies, movie_to_average_rating
        )
    sorted_genres = sorted(genre_avg_ratings.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_genres[:n])


# ------ TASK 4: USER FOCUSED  --------


# 4.1
def read_user_ratings(f):
    # parameter f: movie ratings file name (e.g. "movieRatingSample.txt")
    # return: dictionary that maps user to list of (movie,rating)
    # WRITE YOUR CODE BELOW

    user_ratings = defaultdict(list)
    with open(f, "r") as file:
        for line in file:
            if line:
                parts = line.split("|")
                if len(parts) == 3:
                    movie, rating, user_id = map(str.strip, parts)
                    user_ratings[user_id].append((movie, float(rating)))
    return user_ratings


# 4.2
def get_user_genre(user_id, user_to_movies, movie_to_genre):
    # parameter user_id: user id
    # parameter user_to_movies: dictionary that maps user to movies and ratings
    # parameter movie_to_genre: dictionary that maps movie to genre
    # return: top genre that user likes
    # WRITE YOUR CODE BELOW

    rated_movies = user_to_movies.get(user_id, [])
    genre_ratings = {}
    
    for movie, rating in rated_movies:
        genre = movie_to_genre.get(movie)
        if genre:
            if genre not in genre_ratings:
                genre_ratings[genre] = []
            genre_ratings[genre].append(rating)
    
    avg_genre_ratings = {}
    for genre, ratings in genre_ratings.items():
        avg_genre_ratings[genre] = sum(ratings) / len(ratings)
    
    top_genre = max(avg_genre_ratings, key=avg_genre_ratings.get)
    
    return top_genre


# 4.3
def recommend_movies(user_id, user_to_movies, movie_to_genre, movie_to_average_rating):
    # parameter user_id: user id
    # parameter user_to_movies: dictionary that maps user to movies and ratings
    # parameter movie_to_genre: dictionary that maps movie to genre
    # parameter movie_to_average_rating: dictionary that maps movie to average rating
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW

    top_genre = get_user_genre(user_id, user_to_movies, movie_to_genre)
    
    movies_in_genre = {movie for movie, genre in movie_to_genre.items() if genre == top_genre}
    
    rated_movies = {movie for movie, _ in user_to_movies.get(user_id, [])}
    unrated_movies = movies_in_genre - rated_movies
    
    recommended = {
        movie: movie_to_average_rating[movie] 
        for movie in unrated_movies if movie in movie_to_average_rating
    }
    sorted_recommended = dict(sorted(recommended.items(), key=lambda x: x[1], reverse=True))
    
    return dict(list(sorted_recommended.items())[:3])


# -------- main function for your testing -----
def main():
    # write all your test code here
    # this function will be ignored by us when grading

   # Path to the sample files
    rating_file = 'movieRatingSample.txt'
    genre_file = 'genreMovieSample.txt'

# ------ TASK 1: READING DATA --------

# Read the ratings and genre data
    ratings_data = read_ratings_data(rating_file)
    movie_genres = read_movie_genre(genre_file)

# Print the ratings data
    print("Ratings Data:")
    print(ratings_data)

# Print the movie genres
    print("\nMovie Genres:")
    print(movie_genres)


# ------ TASK 2: PROCESSING DATA --------

# Create a genre dictionary
    genre_dict = create_genre_dict(movie_genres)
    print("\nGenre Dictionary:")
    print(genre_dict)

# Calculate average ratings
    average_ratings = calculate_average_rating(ratings_data)
    print("\nAverage Ratings:")
    print(average_ratings)


# ------ TASK 3: RECOMMENDATION --------

# Get top 10 popular movies by average rating
    popular_movies = get_popular_movies(average_ratings, 10)
    print("\nTop 10 Popular Movies by Average Rating:")
    print(popular_movies)

# Filter movies with ratings >= 3
    filtered_movies = filter_movies(average_ratings, 3)
    print("\nMovies with Ratings >= 3:")
    print(filtered_movies)

# Get top 5 popular movies in the "Action" genre
    popular_action_movies = get_popular_in_genre('Action', genre_dict, average_ratings, 5)
    print("\nTop 5 Popular Action Movies:")
    print(popular_action_movies)

# Get average rating for the "Adventure" genre
    adventure_rating = get_genre_rating('Adventure', genre_dict, average_ratings)
    print("\nAverage Rating for Adventure Movies:")
    print(adventure_rating)

# Get top 5 most popular genres
    genre_popularity_result = genre_popularity(genre_dict, average_ratings, 5)
    print("\nTop 5 Most Popular Genres:")
    print(genre_popularity_result)


# ------ TASK 4: USER FOCUSED --------

# Read the user ratings data
    user_ratings = read_user_ratings(rating_file)
    print("\nUser Ratings Data:")
    print(user_ratings)

# Get top genre liked by user "6"
    top_genre_user_6 = get_user_genre('6', user_ratings, movie_genres)
    print("\nTop Genre Liked by User 6:")
    print(top_genre_user_6)

# Get movie recommendations for user "6"
    recommended_movies = recommend_movies('11', user_ratings, movie_genres, average_ratings)
    print("\nRecommended Movies for User 6:")
    print(recommended_movies)

# DO NOT write ANY CODE (including variable names) outside of any of the above functions
# In other words, ALL code your write (including variable names) MUST be inside one of
# the above functions

# program will start at the following main() function call
# when you execute hw1.py
main()