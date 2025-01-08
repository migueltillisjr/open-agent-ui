#######################################################################################
# Assistant Common - relevant libs                                                    #
#######################################################################################
from flask import send_file,request, jsonify, render_template, send_from_directory, session, send_from_directory
from werkzeug.utils import secure_filename
import os
from flask import redirect, url_for, flash, request, jsonify, render_template, render_template_string
from flask_login import login_user, login_required, logout_user, current_user
import json
import time
# from .. import Assistant
import uuid

#######################################################################################
# ldmg - relevant libs                                                                #
#######################################################################################
from functools import wraps
from ..config import app, login_manager, db, bcrypt, app_workdir, current_user
from ..models import User, Chat, Message, EmailDesign
# from ..forms import *
# from .email_campaigns import *
# from .email_design import *
# from .files import *
# from .reporting import *
# from .user import *
# from .web_view import *
# from .chat_mgmt import *

# Initialize the database
@app.before_request
def create_tables():
    if not hasattr(create_tables, 'initialized'):
        db.create_all()
        create_tables.initialized = True


