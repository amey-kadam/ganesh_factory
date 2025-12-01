# models.py
from extensions import db
from datetime import date

class Labor(db.Model):
    __tablename__ = "labors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    id_no = db.Column(db.String(50), unique=True, nullable=False)
    phone_no = db.Column(db.String(15), nullable=False)

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

    labor = db.relationship("Labor", back_populates="attendances")
