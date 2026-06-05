import requests
import json

def handler(request = None):
    # Vercel ka format
    if request and 'query' in request:
        query = request.get('query', {})
        api_key = query.get('api_key', '')
        number = query.get('number', '')
    else:
        # Local testing ke liye
        from urllib.parse import parse_qs
        import os
        query_string = os.environ.get('QUERY_STRING', '')
        params = parse_qs(query_string)
        api_key = params.get('api_key', [''])[0]
        number = params.get('number', [''])[0]
    
    # Validate API key
    if api_key != 'leekdata':
        return {
            'statusCode': 401,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 'error', 'message': 'Invalid API key'})
        }
    
    # Validate number
    if not number or len(number) != 10 or not number.isdigit():
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 'error', 'message': '10-digit number required'})
        }
    
    try:
        # Fetch real data
        response = requests.get(
            'https://number-to-api-team-only.vercel.app/api/index.js',
            params={'api_key': 'team6months', 'number': number},
            timeout=10,
            headers={
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36'
            }
        )
        
        data = response.json()
        
        # Clean response - remove unwanted fields
        if 'timestamp' in data:
            del data['timestamp']
        if 'count' in data:
            del data['count']
        
        # Change developer name
        data['developer'] = 'RedRose Member'
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(data)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 'error', 'message': str(e)})
        }
