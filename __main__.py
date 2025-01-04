from .routes import *
from .forms import *
from .tasks import start_scheduler

if __name__ == '__main__':
    # Create the application context and initialize the database tables
    with app.app_context():
        # start_scheduler()
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)