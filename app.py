from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_code', methods=['POST'])
def generate_code_route():
    data = request.json
    requirements = data.get('requirements')
    generated_code = generate_code_from_github(requirements)
    return jsonify({'code': generated_code})

def generate_code_from_github(requirements):
    if not GITHUB_TOKEN:
        return "Please try again later. 🙏🙏🙏"

    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3.raw'
    }
    params = {
        'q': f'{requirements} in:file',
        'per_page': 5
    }
    try:
        response = requests.get('https://api.github.com/search/code', headers=headers, params=params)
        response.raise_for_status() 
        results = response.json()
        for item in results.get('items', []):
            repository = item.get('repository', {}).get('full_name')
            path = item.get('path')
            url = f'https://raw.githubusercontent.com/{repository}/master/{path}'
            code_response = requests.get(url, headers=headers)
            if code_response.status_code == 200:
                return code_response.text
        return "No code generate found for the given requirements. Please try again later. 🙏🙏🙏"
    except requests.RequestException as e:
        return f"Error generate code: {e} Please try again later. 🙏🙏🙏"


if __name__ == '__main__':
    app.run(debug=True)
