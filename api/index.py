from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuration from captured data
API_URL = "https://number-to-api-team-only.vercel.app/api/index.js"
API_KEY = "team6months"

def fetch_number_data(number):
    """
    Fetch real data from the external API
    """
    try:
        params = {
            'api_key': API_KEY,
            'number': number
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en;q=0.9',
            'Referer': 'https://mobile-number-lookup.blogspot.com/'
        }
        
        response = requests.get(
            API_URL,
            params=params,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                'status': 'error',
                'message': f'API returned status code {response.status_code}',
                'code': response.status_code
            }
            
    except requests.exceptions.RequestException as e:
        return {
            'status': 'error',
            'message': f'Request failed: {str(e)}'
        }
    except json.JSONDecodeError as e:
        return {
            'status': 'error',
            'message': f'Failed to parse response: {str(e)}'
        }

@app.route('/api/number/<number>', methods=['GET'])
def get_number_info(number):
    # Validate number
    if not number or not number.isdigit() or len(number) != 10:
        return jsonify({
            'status': 'error',
            'message': 'Invalid mobile number. Please provide a 10-digit number.'
        }), 400
    
    # Fetch real data from external API
    result = fetch_number_data(number)
    
    # Clean the response - remove all extra fields
    if isinstance(result, dict):
        # Remove timestamp
        if 'timestamp' in result:
            del result['timestamp']
        # Remove server_timestamp
        if 'server_timestamp' in result:
            del result['server_timestamp']
        # Remove endpoint
        if 'endpoint' in result:
            del result['endpoint']
        # Remove count
        if 'count' in result:
            del result['count']
        # Change developer name
        if 'developer' in result:
            result['developer'] = 'RedRose Member'  # 🔥 Naya naam set
    
    return jsonify(result), 200 if result.get('status') != 'error' else 502

@app.route('/api/bulk', methods=['POST'])
def bulk_lookup():
    data = request.get_json()
    
    if not data or 'numbers' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Please provide a JSON object with "numbers" array'
        }), 400
    
    numbers = data['numbers']
    if not isinstance(numbers, list):
        return jsonify({
            'status': 'error',
            'message': '"numbers" must be an array'
        }), 400
    
    results = []
    for number in numbers:
        if number and str(number).isdigit() and len(str(number)) == 10:
            result = fetch_number_data(str(number))
            # Clean each result
            if isinstance(result, dict):
                if 'timestamp' in result:
                    del result['timestamp']
                if 'server_timestamp' in result:
                    del result['server_timestamp']
                if 'endpoint' in result:
                    del result['endpoint']
                if 'count' in result:
                    del result['count']
                if 'developer' in result:
                    result['developer'] = 'RedRose Member'
            results.append({
                'number': number,
                'data': result
            })
        else:
            results.append({
                'number': number,
                'error': 'Invalid number format',
                'data': None
            })
    
    return jsonify({
        'status': 'success',
        'total_queried': len(numbers),
        'results': results
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'Mobile Number Lookup API',
        'version': '1.0.0'
    }), 200

@app.route('/api/test', methods=['GET'])
def test_api():
    test_number = "9572691440"
    result = fetch_number_data(test_number)
    
    # Clean test response
    if isinstance(result, dict):
        if 'timestamp' in result:
            del result['timestamp']
        if 'server_timestamp' in result:
            del result['server_timestamp']
        if 'endpoint' in result:
            del result['endpoint']
        if 'count' in result:
            del result['count']
        if 'developer' in result:
            result['developer'] = 'RedRose Member'
    
    return jsonify({
        'test': 'Sample API call',
        'sample_number': test_number,
        'response': result
    }), 200

if __name__ == '__main__':
    print("=" * 50)
    print("Mobile Number Lookup API Server")
    print("=" * 50)
    print("Developer: RedRose Member")
    print("\nAvailable endpoints:")
    print("  GET  /api/number/<number>  - Lookup a single number")
    print("  POST /api/bulk              - Bulk lookup multiple numbers")
    print("  GET  /api/health            - Health check")
    print("  GET  /api/test              - Test with sample number")
    print("=" * 50)
    
    # if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)

# Yeh line add karo (bilkul last me)
app = app
