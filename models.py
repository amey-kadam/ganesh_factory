# models.py
from datetime import date
from flask_login import UserMixin
from extensions import db, login_manager


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(50), nullable=True)

    # relationships
    users = db.relationship("User", back_populates="company", lazy=True)
    workers = db.relationship("Labor", back_populates="company", lazy=True)
    worker_types = db.relationship("WorkerType", back_populates="company", lazy=True)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="admin")  # 'admin' or 'user'

    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    company = db.relationship("Company", back_populates="users")


class WorkerType(db.Model):
    __tablename__ = "worker_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # e.g. Daily, Hourly, Task-wise
    description = db.Column(db.String(255), nullable=True)

    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    company = db.relationship("Company", back_populates="worker_types")

    labors = db.relationship("Labor", back_populates="worker_type", lazy=True)


class Labor(db.Model):
    __tablename__ = "labors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    id_no = db.Column(db.String(50), unique=True, nullable=False)
    phone_no = db.Column(db.String(15), nullable=False)

    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    company = db.relationship("Company", back_populates="workers")

    worker_type_id = db.Column(db.Integer, db.ForeignKey("worker_types.id"), nullable=True)
    worker_type = db.relationship("WorkerType", back_populates="labors")

    attendances = db.relationship("Attendance", back_populates="labor", lazy=True)


class Attendance(db.Model):
    __tablename__ = "attendances"

    id = db.Column(db.Integer, primary_key=True)
    labor_id = db.Column(db.Integer, db.ForeignKey("labors.id"), nullable=False)

    work_date = db.Column(db.Date, nullable=False, default=date.today)
    labor_type = db.Column(db.String(20), nullable=False)
    wage_amount = db.Column(db.Numeric(10, 2), nullable=False)

    hours_worked = db.Column(db.Float, nullable=True)
    tasks_done = db.Column(db.Integer, nullable=True)

    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    company = db.relationship("Company")

    labor = db.relationship("Labor", back_populates="attendances")


@login_manager.user_loader
def load_user(user_id: str):
    try:
        return User.query.get(int(user_id))
    except (TypeError, ValueError):
        return None
