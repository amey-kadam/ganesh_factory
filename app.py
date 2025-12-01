# app.py
from flask import Flask, redirect, url_for
from config import Config
from extensions import db
from models import Labor, Attendance  # make sure models are imported


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # init SQLAlchemy
    db.init_app(app)

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

    # 👇 THIS is the important part: create tables on startup
    with app.app_context():
        db.create_all()

    return app


# for gunicorn (Render)
app = create_app()

# for local run: python app.py
if __name__ == "__main__":
    app.run(debug=True)
