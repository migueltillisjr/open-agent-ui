from . import *
from .. import assistant

###########################################################################################
# Chat Management                                                                         #
###########################################################################################

# Route to create a new chat, associated with the current user
@app.route('/chat/new', methods=['POST'])
##@login_required
def new_chat():
    # Create a new chat
    user_id = current_user.id  # Assuming current_user is the logged-in user
    chat = Chat(user_id=user_id)
    db.session.add(chat)
    db.session.commit()
    
    # Return the composite key values
    return jsonify({"user_id": chat.user_id, "chat_number": chat.chat_number})


# Route to send a message and get a response for a specific chat
@app.route('/chat/<int:user_id>/<int:chat_number>/send', methods=['POST'])
##@login_required
def send_message(user_id, chat_number):
    chat = Chat.query.filter_by(user_id=user_id, chat_number=chat_number).first_or_404()
    data = request.json
    user_message = data.get("message")

    # Save the user message to the database
    user_msg = Message(user_id=user_id, chat_number=chat_number, sender="user", content=user_message)
    db.session.add(user_msg)

    # Get assistant response
    assistant_response = assistant(user_id=current_user.id)

    # Save the assistant response
    assistant_msg = Message(user_id=user_id, chat_number=chat_number, sender="assistant", content=assistant_response)
    db.session.add(assistant_msg)
    db.session.commit()

    return jsonify({
        "user_id": user_id,
        "chat_number": chat_number,
        "user_message": user_message,
        "assistant_message": assistant_response
    })


# Route to get the chat history for a specific chat
@app.route('/chat/<int:user_id>/<int:chat_number>/history', methods=['GET'])
##@login_required
def get_chat_history(user_id, chat_number):
    chat = Chat.query.filter_by(user_id=user_id, chat_number=chat_number).first_or_404()
    messages = Message.query.filter_by(user_id=user_id, chat_number=chat_number).order_by(Message.timestamp).all()

    return jsonify({
        "user_id": user_id,
        "chat_number": chat_number,
        "messages": [
            {"sender": msg.sender, "message": msg.content, "timestamp": msg.timestamp} for msg in messages
        ]
    })


# Route to get the list of all chats for the current user
@app.route('/chat-history', methods=['GET'])
##@login_required
def get_chat_list():
    chats = Chat.query.filter_by(user_id=current_user.id).all()
    chat_list = [
        {"user_id": chat.user_id, "chat_number": chat.chat_number, "created_at": chat.created_at} for chat in chats
    ]
    return jsonify({"chats": chat_list})


# Route to delete a chat for the current user
@app.route('/chat/<int:user_id>/<int:chat_number>/delete', methods=['DELETE'])
##@login_required
def delete_chat(user_id, chat_number):
    chat = Chat.query.filter_by(user_id=user_id, chat_number=chat_number).first_or_404()
    db.session.delete(chat)
    db.session.commit()
    return jsonify({"success": True})
