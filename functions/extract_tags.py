# functions/extract_tags.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS extension
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/.netlify/functions/extract_tags', methods=['POST', 'OPTIONS'])
def extract_tags():
    if request.method == 'OPTIONS':
        # Respond to preflight request
        return '', 200

    data = request.get_json()
    video_url = data.get('video_url')

    if not video_url:
        return jsonify({"error": "Missing 'video_url' parameter"}), 400

    try:
        response = requests.get(video_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        soup = BeautifulSoup(response.text, 'html.parser')
        tags_meta_list = soup.find_all('meta', {'property': 'og:video:tag'})

        if tags_meta_list:
            all_tags = [tag['content'].strip() for tag in tags_meta_list]
            return jsonify({"tags": all_tags})
        else:
            return jsonify({"tags": []})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
