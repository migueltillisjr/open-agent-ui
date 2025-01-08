import requests

# Define the base URL of the Flask app
BASE_URL = "http://127.0.0.1:5000"

# Define the signup endpoint
SIGNUP_ENDPOINT = f"{BASE_URL}/signup"

# Define the payload for the signup request
payload = {
    "username": "testuser",
    "password": "password123",
    "confirm_password": "password123"
}

# Make the POST request to the signup route
response = requests.post(SIGNUP_ENDPOINT, data=payload)

# Print the response
if response.ok:
    print("Signup successful!")
    print("Response:", response.text)
else:
    print("Signup failed.")
    print("Status Code:", response.status_code)
    print("Response:", response.text)