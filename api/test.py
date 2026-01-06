"""
Simple test endpoint to verify Vercel deployment
"""

def app(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'application/json')]
    start_response(status, headers)
    return [b'{"status": "ok", "message": "Test endpoint works"}']
