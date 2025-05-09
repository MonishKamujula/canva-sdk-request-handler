from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

def search_pexels_image(query):
    headers = {
        "Authorization": os.environ.get("PEXELS_API_KEY")
    }
    params = {
        "query": query,
        "per_page": 1
    }
    response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
    return response.json()['photos'][0]['src']['medium']

@app.route('/search-image', methods=['GET'])
def search_image():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    image_url = search_pexels_image(query)
    return  f"<img src={image_url}>"

if __name__ == "__main__":
    app.run(port=5001)

