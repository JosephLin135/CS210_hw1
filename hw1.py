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

    try:
        with open(f, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split("|")

                    if len(parts) == 3:
                        movie, rating, _ = parts
                        try:
                            ratings_data[movie].append(float(rating))
                        except ValueError:
                            continue

    except FileNotFoundError:
        return {}
    except Exception:
        return {}

    return ratings_data


# 1.2
def read_movie_genre(f):
    # parameter f: movies genre file name f (e.g. "genreMovieSample.txt")
    # return: dictionary that maps movie to genre
    # WRITE YOUR CODE BELOW

    movie_genres = {}

    try:
        with open(f, "r") as file:
            for line in file:
                line = line.strip()
                if line:  # Proceed only if the line is not empty
                    parts = line.split("|")

                    if len(parts) == 3:  # Expecting genre|user_id|movie
                        genre, _, movie = parts
                        movie_genres[movie.strip()] = genre.strip()

    except FileNotFoundError:
        return {}
    except Exception:
        return {}

    return movie_genres


# ------ TASK 2: PROCESSING DATA --------


# 2.1
def create_genre_dict(d):
    # parameter d: dictionary that maps movie to genre
    # return: dictionary that maps genre to movies
    # WRITE YOUR CODE BELOW

    genre_dict = defaultdict(list)
    for movie, genre in d.items():
        genre_dict[genre].append(movie)
    return genre_dict


# 2.2
def calculate_average_rating(d):
    # parameter d: dictionary that maps movie to ratings
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW

    average_ratings = {}
    for movie, ratings in d.items():
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
            user_id, movie, rating = line.strip().split()
            user_ratings[user_id].append((movie, float(rating)))
    return user_ratings


# 4.2
def get_user_genre(user_id, user_to_movies, movie_to_genre):
    # parameter user_id: user id
    # parameter user_to_movies: dictionary that maps user to movies and ratings
    # parameter movie_to_genre: dictionary that maps movie to genre
    # return: top genre that user likes
    # WRITE YOUR CODE BELOW
    movie_ratings = user_to_movies.get(user_id, [])
    genre_count = Counter()
    for movie, rating in movie_ratings:
        genre = movie_to_genre.get(movie)
        if genre:
            genre_count[genre] += 1
    return genre_count.most_common(1)[0][0] if genre_count else None


# 4.3
def recommend_movies(user_id, user_to_movies, movie_to_genre, movie_to_average_rating):
    # parameter user_id: user id
    # parameter user_to_movies: dictionary that maps user to movies and ratings
    # parameter movie_to_genre: dictionary that maps movie to genre
    # parameter movie_to_average_rating: dictionary that maps movie to average rating
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW
    rated_movies = {movie for movie, _ in user_to_movies.get(user_id, [])}
    recommended = {
        movie: rating
        for movie, rating in movie_to_average_rating.items()
        if movie not in rated_movies
    }
    return dict(sorted(recommended.items(), key=lambda x: x[1], reverse=True))


# -------- main function for your testing -----
def main():
    # write all your test code here
    # this function will be ignored by us when grading

    # Test 1: Reading ratings data
    print("Testing read_ratings_data()")
    ratings_data = read_ratings_data("movieRatingSample.txt")
    print(f"Ratings data (sample): {dict(list(ratings_data.items())[::])}")
    print("Test Passed!" if ratings_data else "Test Failed!")

    # Test 2: Reading movie genres
    print("\nTesting read_movie_genre()")
    movie_genres = read_movie_genre("genreMovieSample.txt")
    print(f"Movie genres (sample): {dict(list(movie_genres.items())[::])}")
    print("Test Passed!" if movie_genres else "Test Failed!")

    # Test 3: Creating genre dictionary
    print("\nTesting create_genre_dict()")
    genre_dict = create_genre_dict(movie_genres)
    print(f"Genre dictionary (sample): {dict(list(genre_dict.items())[::])}")
    print("Test Passed!" if genre_dict else "Test Failed!")

    # Test 4: Calculating average ratings
    print("\nTesting calculate_average_rating()")
    average_ratings = calculate_average_rating(ratings_data)
    print(f"Average ratings (sample): {dict(list(average_ratings.items())[::])}")
    print("Test Passed!" if average_ratings else "Test Failed!")

    # Test 5: Getting popular movies (Top 5)
    print("\nTesting get_popular_movies()")
    popular_movies = get_popular_movies(average_ratings, 5)
    print(f"Popular movies (top 5): {popular_movies}")
    print("Test Passed!" if popular_movies else "Test Failed!")

    # Test 6: Filtering movies with ratings >= 4
    print("\nTesting filter_movies()")
    filtered_movies = filter_movies(average_ratings, 4)
    print(f"Movies with rating >= 4: {filtered_movies}")
    print("Test Passed!" if filtered_movies else "Test Failed!")

    # Test 7: Getting popular movies in a specific genre (e.g., Comedy)
    print("\nTesting get_popular_in_genre()")
    popular_comedy_movies = get_popular_in_genre("Comedy", genre_dict, average_ratings)
    print(f"Popular comedy movies: {popular_comedy_movies}")
    print("Test Passed!" if popular_comedy_movies else "Test Failed!")

    # Test 8: Getting average rating for a specific genre (e.g., Comedy)
    print("\nTesting get_genre_rating()")
    comedy_genre_rating = get_genre_rating("Comedy", genre_dict, average_ratings)
    print(f"Average rating for 'Comedy' genre: {comedy_genre_rating}")
    print("Test Passed!" if comedy_genre_rating else "Test Failed!")

    # Test 9: Calculating genre popularity
    print("\nTesting genre_popularity()")
    genre_popularity_scores = genre_popularity(genre_dict, average_ratings)
    print(f"Genre popularity (by average ratings): {genre_popularity_scores}")
    print("Test Passed!" if genre_popularity_scores else "Test Failed!")


# DO NOT write ANY CODE (including variable names) outside of any of the above functions
# In other words, ALL code your write (including variable names) MUST be inside one of
# the above functions

# program will start at the following main() function call
# when you execute hw1.py
main()
