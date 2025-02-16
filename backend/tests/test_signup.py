import requests

api_url = "http://127.0.0.1:8000/"

test_data = {
    "email": "test2@example.com",
    "username": "testuser2",
    "password": "password12345"
}

print(f"Attempting to sign up...")

response = requests.post(api_url + "signup", json=test_data)

print(f"Response: {response}")