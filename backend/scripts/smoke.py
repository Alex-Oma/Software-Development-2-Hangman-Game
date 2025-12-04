import urllib.request
import json

# This is simple smoke test to check if the backend is running and responding to HTTP requests
url = 'http://127.0.0.1:8000/static/index.html'

# Make a request to the backend
try:
    # timeout after 5 seconds
    with urllib.request.urlopen(url, timeout=5) as r:
        # read the response body
        body = r.read().decode('utf-8')
        # print status and body
        print('status', r.status)
        # attempt to parse as json
        try:
            # print as json if possible
            print('json:', json.loads(body))
        except Exception:
            # not json, print raw body
            print('body:', body)
except Exception as e:
    # print error
    print('error', e)

