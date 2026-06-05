from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/index.py', methods=['GET'])
def handle():
    api_key = request.args.get('api_key')
    number = request.args.get('number')
    
    if api_key != 'leekdata':
        return jsonify({'status': 'error', 'message': 'Invalid API key'}), 401
    
    if not number or len(number) != 10 or not number.isdigit():
        return jsonify({'status': 'error', 'message': '10-digit number required'}), 400
    
    try:
        resp = requests.get(
            'https://number-to-api-team-only.vercel.app/api/index.js',
            params={'api_key': 'team6months', 'number': number},
            timeout=10
        )
        data = resp.json()
        
        # Clean
        data.pop('timestamp', None)
        data.pop('count', None)
        data['developer'] = 'RedRose Member'
        
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

app = app  # Vercel ke liye
