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
        'Accept': 'application/vnd.github.v3+json'
    }
    
    file_extensions = [
        'html', 'css','py', 'java', 'cpp', 'c', 'cs', 'js', 'ts', 'php', 'rb', 'go', 'pl', 'scala', 'groovy', 'r', 'swift', 'kotlin', 'rust', 'lua', 'm', 'asm', 'h', 'hpp', 's', 'vhdl', 'f', 'f90', 'f95', 'pas', 'lisp', 'ml', 'hs', 'erl', 'dart', 'vala', 'd', 'rkt', 'julia', 'nim', 'tcl', 'awk', 'fortran', 'ada', 'ocaml', 'matlab'
    ]
    query = f'{requirements} in:file ' + ' '.join([f'extension:{ext}' for ext in file_extensions])
    
    params = {
        'q': query,
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
            code_response = requests.get(url, headers={'Authorization': f'token {GITHUB_TOKEN}'})
            if code_response.status_code == 200:
                return code_response.text
        return "No suitable code found for the given requirements. Please try again later. 🙏🙏🙏"
    except requests.RequestException as e:
        return f"Please try again later. 🙏🙏🙏"

if __name__ == '__main__':
    app.run(debug=True)
