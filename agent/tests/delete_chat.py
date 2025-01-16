import requests

# Configuration
BASE_URL = "http://localhost:5000"  # Replace with your server's URL
USER_ID = 1  # Replace with a valid user ID
CHAT_NUMBER = 2  # Replace with a valid chat number

def test_delete_chat(user_id, chat_number):
    """Tests the DELETE /chat/{userId}/{chatNumber} API."""
    url = f"{BASE_URL}/chat/{user_id}/{chat_number}/delete"
    
    try:
        # Send the DELETE request
        response = requests.delete(url)
        
        # Print the status and response details
        if response.status_code == 200:
            print(f"Chat {chat_number} for user {user_id} deleted successfully.")
        else:
            print(f"Failed to delete chat. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending the DELETE request: {e}")

if __name__ == "__main__":
    # Run the test
    test_delete_chat(USER_ID, CHAT_NUMBER)
