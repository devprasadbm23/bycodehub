from flask import Flask, render_template
from config import Config
from extensions import db, mail, migrate
from routes import main, admin
from models import Admin
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')
    
    # Error handlers
    register_error_handlers(app)
    
    # Create default admin (if needed) - this should ideally be a CLI command or separate script
    with app.app_context():
        # Ensure tables exist (legacy mode, in real prod use migrations)
        # db.create_all() # Commented out in favor of migrations, but kept for safe transition if needed
        pass

    return app

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

app = create_app()

# Initial setup helper (optional, can be removed)
@app.cli.command("init-db")
def init_db():
    db.create_all()
    if not Admin.query.filter_by(username=app.config['ADMIN_USERNAME']).first():
        admin_user = Admin(username=app.config['ADMIN_USERNAME'])
        admin_user.set_password(app.config['ADMIN_PASSWORD'])
        db.session.add(admin_user)
        db.session.commit()
        print("Initialized database and default admin.")
    else:
        print("Database already initialized.")

if __name__ == '__main__':
    with app.app_context():
        # Check if DB needs init (simple check)
        if not os.path.exists('bycodehub.db'):
            db.create_all()
            if not Admin.query.filter_by(username='admin').first():
                 # Create default admin from config
                admin_user = Admin(username=app.config['ADMIN_USERNAME'])
                admin_user.set_password(app.config['ADMIN_PASSWORD'])
                db.session.add(admin_user)
                db.session.commit()
                print("Created default admin.")

    app.run(debug=True)