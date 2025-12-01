# app.py
from flask import Flask, redirect, url_for
from config import Config
from extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # init SQLAlchemy
    db.init_app(app)

    # import models so SQLAlchemy knows them
    from models import Labor, Attendance

    # import and register blueprints
    from labor import labor_bp
    from admin_panel import admin_bp
    from reports import reports_bp

    app.register_blueprint(labor_bp, url_prefix="/labor")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(reports_bp, url_prefix="/reports")

    @app.route("/")
    def index():
        return redirect(url_for("labor.register_labor"))

    # 👇 Route to manually initialize DB tables on Render
    @app.route("/init-db")
    def init_db():
        # This will create all tables if they don't exist
        db.create_all()
        return "Database tables created (or already existed)."

    # Optional: also create tables on startup (does nothing if tables already exist)
    with app.app_context():
        db.create_all()

    return app


# For gunicorn / Render
app = create_app()

# For local debugging
if __name__ == "__main__":
    app.run(debug=True)
