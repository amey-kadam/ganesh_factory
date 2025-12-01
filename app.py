# app.py
from flask import Flask, redirect, url_for
from config import Config
from extensions import db, migrate

# Make sure models are imported so Flask-Migrate can see them
from models import Labor, Attendance


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints (3 modules)
    from labor import labor_bp
    from admin_panel import admin_bp
    from reports import reports_bp

    app.register_blueprint(labor_bp, url_prefix="/labor")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(reports_bp, url_prefix="/reports")

    @app.route("/")
    def index():
        # Redirect to labor registration or dashboard as you like
        return redirect(url_for("labor.register_labor"))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
