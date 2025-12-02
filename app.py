# app.py
from flask import Flask, redirect, url_for
from config import Config
from extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # init extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # where to redirect if not logged in

    # import models so SQLAlchemy knows them
    from models import Company, User, WorkerType, Labor, Attendance

    # import and register blueprints
    from labor import labor_bp
    from admin_panel import admin_bp
    from reports import reports_bp
    from auth import auth_bp
    from settings_bp import settings_bp
    from attendance_import import attendance_import_bp
    from main import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(settings_bp, url_prefix="/settings")
    app.register_blueprint(attendance_import_bp, url_prefix="/admin/import")
    app.register_blueprint(labor_bp, url_prefix="/labor")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(reports_bp, url_prefix="/reports")

    @app.route("/")
    def index():
        # home – redirect to login, then login will redirect as needed
        return redirect(url_for("auth.login"))

    @app.route("/init-db")
    def init_db():
        # This will create all tables if they don't exist
        db.create_all()
        return "Database tables created (or already existed)."

    # Also create tables on startup (safe to call multiple times)
    with app.app_context():
        db.create_all()

    return app


# For gunicorn / Render
app = create_app()

# For local debugging
if __name__ == "__main__":
    app.run(debug=True)
