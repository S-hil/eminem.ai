import requests

url = "https://api.d-id.com/talks"

payload = {
    "script": {
        "type": "text",
        "provider": {
            "type": "microsoft",
            "voice_id": "Jenny"
        },
        "ssml": "false"
    },
    "config": {
        "fluent": "false",
        "pad_audio": "0.0"
    }
}
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)