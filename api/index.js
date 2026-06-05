export default async function handler(req, res) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }
  
  // Get query parameters
  const { api_key, number } = req.query;
  
  // Validate API key
  if (api_key !== 'database') {
    return res.status(401).json({
      status: 'error',
      message: 'Invalid API key'
    });
  }
  
  // Validate number
  if (!number || !/^\d{10}$/.test(number)) {
    return res.status(400).json({
      status: 'error',
      message: 'Please provide a valid 10-digit mobile number'
    });
  }
  
  try {
    // Fetch real data from the original API
    const fetch = (await import('node-fetch')).default;
    
    const response = await fetch(
      `https://heated-reconstruction-till-amy.trycloudflare.com/search?query=${number}`,
      {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36'
        }
      }
    );
    
    const data = await response.json();
    
    // Clean the response - remove unwanted fields
    delete data.timestamp;
    delete data.count;
    delete data.server_timestamp;
    delete data.endpoint;
    delete data.cached;
    delete data.credit;
    delete data.type;
    
    // Change developer name
    data.developer = 'ColdenMack';
    
    // Return success response
    return res.status(200).json(data);
    
  } catch (error) {
    console.error('Fetch error:', error);
    return res.status(500).json({
      status: 'error',
      message: 'Failed to fetch data. Please try again later.',
      error: error.message
    });
  }
}
