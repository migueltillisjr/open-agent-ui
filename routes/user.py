from . import *
from ..tasks import create_directory_structure

app_files = os.getenv('APP_FILES')

# Base directory for user and design files
USERS_BASE_DIR = "users"
os.makedirs(f'{app_files}/users', exist_ok=True)

###########################################################################################
# User Management                                                                         #
###########################################################################################

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Redirect to the main page after login
        else:
            flash('Login failed. Check your username and password.', 'error')
    return render_template('login.html', form=form)

# Helper function to create a directory for a new user
def create_user_directory(user_id):
    user_dir = f'{app_files}/users/{user_id}'
    os.makedirs(user_dir, exist_ok=True)
    create_directory_structure(user_dir)
    return user_dir

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        try:
            # Hash password
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            
            # Create a new user instance
            new_user = User(username=form.username.data, password=hashed_password, directory_path="")
            db.session.add(new_user)
            db.session.commit()
            
            # Create a directory for the new user and update the user's directory_path
            user_dir = create_user_directory(new_user.id)
            new_user.directory_path = user_dir
            db.session.commit()
            
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            flash('Signup failed. Try again or choose a different username.', 'error')
    return render_template('signup.html', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()  # Clear all session data
    flash('You have been logged out successfully.', 'success')  # Add a specific flash message for logout
    return redirect(url_for('login'))


