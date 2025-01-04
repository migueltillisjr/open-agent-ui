import requests

BASE_URL = "http://127.0.0.1:5000"

# Helper function to create a user session (if required)
def login_and_get_session():
    session = requests.Session()
    login_response = session.post(
        f"{BASE_URL}/login", 
        data={"username": "miguel", "password": "asdfasdf"}
    )
    if login_response.status_code != 200:
        raise Exception("Login failed. Check your username and password.")
    return session

def test_new_chat():
    try:
        session = login_and_get_session()
        response = session.post(f"{BASE_URL}/chat/new")
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        data = response.json()
        print(data)
        assert "user_id" in data and "chat_number" in data, "Response missing required keys"
        return data
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except AssertionError as e:
        print(f"Assertion failed: {e}")

if __name__ == "__main__":
    chat_data = test_new_chat()
    if chat_data:
        print(f"New chat created: {chat_data}")


# def test_send_message(chat_data):
#     session = login_and_get_session()
#     user_id, chat_number = chat_data["user_id"], chat_data["chat_number"]
#     response = session.post(
#         f"{BASE_URL}/chat/{user_id}/{chat_number}/send",
#         json={"message": "Hello, assistant!"}
#     )
#     assert response.status_code == 200
#     data = response.json()
#     print(data)
#     assert data["user_message"] == "Hello, assistant!"
#     assert "assistant_message" in data

# def test_get_chat_history(chat_data):
#     session = login_and_get_session()
#     user_id, chat_number = chat_data["user_id"], chat_data["chat_number"]
#     response = session.get(f"{BASE_URL}/chat/{user_id}/{chat_number}/history")
#     assert response.status_code == 200
#     data = response.json()
#     print(data)
#     assert "messages" in data and len(data["messages"]) > 0

# def test_get_chat_list():
#     session = login_and_get_session()
#     response = session.get(f"{BASE_URL}/chat-history")
#     assert response.status_code == 200
#     data = response.json()
#     print(data)
#     assert "chats" in data and len(data["chats"]) > 0

# def test_delete_chat(chat_data):
#     session = login_and_get_session()
#     user_id, chat_number = chat_data["user_id"], chat_data["chat_number"]
#     response = session.delete(f"{BASE_URL}/chat/{user_id}/{chat_number}/delete")
#     assert response.status_code == 200
#     data = response.json()
#     print(data)
#     assert data["success"] is True

if __name__ == "__main__":
    # Run the tests sequentially
    chat_data = test_new_chat()
    # test_send_message(chat_data)
    # test_get_chat_history(chat_data)
    # test_get_chat_list()
    # test_delete_chat(chat_data)
