# system standard
import os

# third party
from dotenv import load_dotenv
import requests 
import urllib.parse

load_dotenv()
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL= "https://image.tmdb.org/t/p"
HEADERS = {
    "accept": "application/json",
    "Authorization": os.environ.get("TMDB_AUTHORIZATION_TOKEN")
    }

def search_any(query, cat="movie", page=1, language="en-US"):
    """
    search for a movie, actor/actress, tv show or company with a keyword
    query: a keyword
    cat: movie, person, tv, company
    page: page number
    language: language code
    """
    url = f"{BASE_URL}/search/{cat}?query={urllib.parse.quote(query)}&include_adult=false&language={language}&page={page}"
    response = requests.get(url, headers=HEADERS).json()
    success = response.get("success", True)
    if success:
        return response["results"], success
    else:
        return response["status_message"], success


def trending(category="movie", time_window="day", page=1, language="en-US"):
    """
    search for trending movies 
    categories: all, movie, tv, person
    time_window: day, week
    """
    url = f"{BASE_URL}/trending/{category}/{time_window}?language={language}&page={page}"
    response = requests.get(url, headers=HEADERS).json()
    success = response.get("success", True)
    if success:
        return response["results"], success
    else:
        return response["status_message"], success
    
def get_list(category, page=1, language="en-US"):
    """
    get movie playlist by category
    category: now_playing, popular, top_rated, upcoming
    """
    url = f"{BASE_URL}/movie/{category}?language={language}&page={page}"
    response = requests.get(url, headers=HEADERS).json()
    success = response.get("success", True)
    if success:
        return response["results"], success
    else:
        return response["status_message"], success

    
def get_image(path, quality="w500"):
    """
    get a url to an image given its path and quality
    path: any
    quality: w92, w154, w185, w342, w500, w780, original
    """
    return f"{IMAGE_BASE_URL}/{quality}{path}"

def search_by_id(id):
    """
    get movie details by id
    """
    url = f"{BASE_URL}/movie/{id}?language=en-US"
    response = requests.get(url, headers=HEADERS).json()
    success = response.get("success", True)
    if success:
        return response, success
    else:
        return response["status_message"], success

def get_credits(movie_id):
    """
    get movie credits by id
    """
    url = f"{BASE_URL}/movie/{movie_id}/credits?language=en-US"
    response = requests.get(url, headers=HEADERS).json()
    success = response.get("success", True)
    if success:
        return response, success
    else:
        return response["status_message"], success
    
movrev = "https://api.themoviedb.org/3/movie/{movie_id}/reviews"

def movie_reviews(movie_id):
    """
    get movie reviews by id
    """
    url = f"{BASE_URL}/movie/{movie_id}/reviews"
    response = requests.get(url, headers=HEADERS).json()
    success = response.get("success", True)
    if success:
        return response["results"], success
    else:
        return response["status_message"], success
    
def get_related_list(movie_id, category="recommendations"):
    """
    gets movie lists that are related to the movie with id=movie_id
    category: similar, recommendations, popular, top_rated
    """
    url = f"{BASE_URL}/movie/{movie_id}/{category}"
    response = requests.get(url, headers=HEADERS).json()
    success = response.get("success", True)
    if success:
        return response["results"], success
    else:
        return response["status_message"], success
    
def get_images(movie_id, res="w500"):
    """
    get movie images by id
    res: w92, w154, w185, w342, w500, w780, original
    """
    url = f"{BASE_URL}/movie/{movie_id}/images"
    response = requests.get(url, headers=HEADERS).json()
    success = response.get("success", True)
    if success:
        return [get_image(image["file_path"], res) for image in response["backdrops"]], success
    else:
        return response["status_message"], success

