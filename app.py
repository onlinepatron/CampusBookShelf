from flask import Flask, render_template
from flask_login import login_required
from extensions import db, migrate, login_manager

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campusbookshelf.db'
    app.config['SECRET_KEY'] = 'supersecretkey'

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        from models import User, Book, Review  # Import models after db has been initialized
        from auth import auth_bp
        from book_routes import book_bp
        from review_routes import review_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(book_bp)
        app.register_blueprint(review_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/main')
    @login_required
    def main():
        return render_template('mainPage.html')

    @app.route('/about-us')
    def about():
        return render_template('aboutUs.html')

    @app.route('/profile')
    def profile():
        return render_template('aboutUs.html')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
