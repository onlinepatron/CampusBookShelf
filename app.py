from flask import Flask, render_template
from flask_login import login_required
from extensions import db, migrate, login_manager
from admin import admin_bp
from models import User

def create_admin():
    admin_username = 'root'
    admin_email = 'root@example.com'
    admin_password = 'root'

    admin_user = User.query.filter_by(username=admin_username).first()
    if not admin_user:
        admin_user = User(username=admin_username, email=admin_email, is_admin=True)
        admin_user.set_password(admin_password)
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user '{admin_username}' created.")
    else:
        print(f"Admin user '{admin_username}' already exists.")

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campusbookshelf.db'
    app.config['SECRET_KEY'] = 'supersecretkey'

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        from auth import auth_bp
        from book_routes import book_bp
        from review_routes import review_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(book_bp)
        app.register_blueprint(review_bp)
        app.register_blueprint(admin_bp)

        db.create_all()
        create_admin()
        
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

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
