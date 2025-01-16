from ..config import db, app
from flask_login import UserMixin
from datetime import datetime

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    directory_path = db.Column(db.String(500), nullable=False)  # Path to the user's directory
    email_designs = db.relationship('EmailDesign', backref='user', cascade='all, delete-orphan', lazy=True)

# EmailDesign model
class EmailDesign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    design_id = db.Column(db.String(50), unique=True, nullable=False)  # Unique design identifier
    html_content = db.Column(db.Text, nullable=False)  # HTML content of the design
    json_content = db.Column(db.JSON, nullable=False)  # JSON content of the design
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Reference to the user

# Chat and Message Models
class Chat(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # Part of composite primary key
    chat_number = db.Column(db.Integer, primary_key=True)  # Sequential ID for each user
    chat_name = db.Column(db.String(255), nullable=True)  # Name of the chat (optional)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('Message', backref='chat', cascade='all, delete-orphan', lazy=True)

    def __init__(self, user_id, chat_name=None):
        self.user_id = user_id
        self.chat_name = chat_name or f"Chat {self.chat_number}"  # Default chat name if none provided

        # Assign chat_number as the next sequential value for this user
        last_chat = Chat.query.filter_by(user_id=user_id).order_by(Chat.chat_number.desc()).first()
        self.chat_number = (last_chat.chat_number + 1) if last_chat else 1


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Foreign key component
    chat_number = db.Column(db.Integer, nullable=False)  # Foreign key component
    sender = db.Column(db.String(50), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Composite foreign key
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['user_id', 'chat_number'], ['chat.user_id', 'chat.chat_number']
        ),
    )


# Image model
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(200), nullable=False)
    image_path = db.Column(db.String(500), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)