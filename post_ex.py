import requests
from service.models import MessageRequest

url = 'http://localhost:8000/send-message/'

payload = {
    "usernames": "@Srnbks,@snowdyDT",
    "message": "Hello!"
}

response = requests.post(url, json=payload)

print(response.status_code)
print(response.json())
