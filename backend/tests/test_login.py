import requests

api_url = "http://127.0.0.1:8000/"

test_data = {
    "email": "test1@example.com",
    "username": "testuser1",
    "password": "password1234"
}

print(f"Attempting to sign up...")

response = requests.post(api_url + "login", json=test_data)

print(f"Response: {response}")