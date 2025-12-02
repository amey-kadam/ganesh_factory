# reports.py
from datetime import datetime, date, timedelta
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from extensions import db
from models import Labor, Attendance

reports_bp = Blueprint("reports", __name__, template_folder="templates")


def _parse_date(date_str, default=None):
    if not date_str:
        return default
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return default


@reports_bp.route("/attendance", methods=["GET"])
@login_required
def attendance_report():
    period = request.args.get("period", "daily")
    date_str = request.args.get("date")
    start_str = request.args.get("start_date")
    end_str = request.args.get("end_date")

    today = date.today()
    base_date = _parse_date(date_str, default=today)

    if period == "daily":
        start_date = end_date = base_date
    elif period == "weekly":
        start_date = base_date - timedelta(days=base_date.weekday())
        end_date = start_date + timedelta(days=6)
    elif period == "monthly":
        start_date = base_date.replace(day=1)
        if base_date.month == 12:
            next_month = base_date.replace(year=base_date.year + 1, month=1, day=1)
        else:
            next_month = base_date.replace(month=base_date.month + 1, day=1)
        end_date = next_month - timedelta(days=1)
    else:  # custom
        start_date = _parse_date(start_str, today)
        end_date = _parse_date(end_str, today)

    query = (
        Attendance.query
        .filter(
            Attendance.company_id == current_user.company_id,
            Attendance.work_date >= start_date,
            Attendance.work_date <= end_date,
        )
        .join(Labor)
        .add_entity(Labor)
        .order_by(Attendance.work_date, Labor.name)
    )

    records = query.all()
    total_wages = sum(float(r.Attendance.wage_amount) for r in records)

    return render_template(
        "reports_attendance.html",
        records=records,
        start_date=start_date,
        end_date=end_date,
        period=period,
        total_wages=total_wages,
    )
