import os
import yaml
from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

#######################################################################################
# Assistant Common - relevant libs                                                                #
#######################################################################################
from flask import abort, Flask, request, jsonify, render_template, send_from_directory, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import schedule
import threading
import shutil
# from assistant import Assistant
import time
# from . import config
from flask_cors import CORS

user_profile_path = os.path.expanduser('~')

class Config:
    def __init__(self, config_path=f'{user_profile_path}/.assistant/openllmui.yaml'):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        self._replace_env_vars(self.config)

    def _replace_env_vars(self, config):
        for key, value in config.items():
            if isinstance(value, dict):
                self._replace_env_vars(value)
            elif isinstance(value, str) and value.startswith('${') and value.endswith('}'):
                env_var = value[2:-1]
                config[key] = os.getenv(env_var, '')

    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, default)
            if value is None:
                return default
        return value

    def set_env_if_not_exists(self, env_var, value):
        if not os.getenv(env_var):
            os.environ[env_var] = value

# Load the configuration
config = Config()

# Set the environment variables only if they are not already set
config.set_env_if_not_exists('OPENAI_API_KEY', config.get('openai.api_key'))
config.set_env_if_not_exists('INSTAGRAM_ACCESS_TOKEN', config.get('instagram.access_token'))
config.set_env_if_not_exists('CLIENT_ID', config.get('reddit.id'))
config.set_env_if_not_exists('CLIENT_SECRET', config.get('reddit.secret'))
config.set_env_if_not_exists('USER_AGENT', config.get('reddit.user_agent'))
config.set_env_if_not_exists('ALPHAVANTAGE_KEY', config.get('alphavantage.key'))
config.set_env_if_not_exists('GPT_DIRECTIONS', config.get('gpt_directions'))
config.set_env_if_not_exists('UI_AUTH', config.get('ui_auth'))
config.set_env_if_not_exists('FINE_TUNING', config.get('fine_tuning'))
config.set_env_if_not_exists('LOG_FILE', config.get('log_file'))
config.set_env_if_not_exists('UPLOAD_FOLDER', config.get('upload_folder'))
config.set_env_if_not_exists('HOST', config.get('host'))
config.set_env_if_not_exists('PORT', config.get('port'))
config.set_env_if_not_exists('APP_FILES', config.get('app_files'))
config.set_env_if_not_exists('APP_WORKDIR', config.get('app_workdir'))
config.set_env_if_not_exists('GOOGLE_AUTH', config.get('google_auth'))
config.set_env_if_not_exists('SQLALCHEMY_DATABASE_URI', config.get('sqlalchemy_database_uri'))
config.set_env_if_not_exists('REPORT_ACCESS_PORT', config.get('report_access_port'))

config.set_env_if_not_exists('REPLY_TO_EMAIL', config.get('reply_to_email'))
config.set_env_if_not_exists('HTML_REPORT_URL', config.get('html_report_url'))
config.set_env_if_not_exists('SENDER_EMAIL', config.get('sender_email'))


#######################################################################################
# Assistant Common - relevant code                                                    #
#######################################################################################
app_workdir = config.get('app_workdir')
current_directory = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=f'{app_workdir}/templates')
app.config['UPLOAD_FOLDER'] = os.environ["UPLOAD_FOLDER"]
app.config['IMGS'] = f"{app_workdir}/imgs/"
app.config['APP-FILES'] = f"{app_workdir}/app-files/"
CORS(app)

# SQLite Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('sqlalchemy_database_uri')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

global db
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login page if not authenticated

fqdn = os.getenv('host')
port = os.getenv('PORT')