import requests
import json

try:
    response = requests.post(
        "http://localhost:8000/chat",
        json={"query": "Vad ska jag göra om Safe tappar GPS?"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
