import requests
import os


def search_pexels_image(query):
    headers = {
        "Authorization": os.environ.get("PIXEL_API_KEY")
    }
    params = {
        "query": query,
        "per_page": 1
    }
    response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
    print(response.json())
    return response.json()['photos'][0]['src']['medium']
