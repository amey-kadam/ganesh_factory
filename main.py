# main.py
from datetime import date
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from extensions import db
from models import Labor, Attendance

main_bp = Blueprint("main", __name__, template_folder="templates")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    """
    Main dashboard showing company statistics and recent activity.
    """
    # Get total workers for this company
    total_workers = Labor.query.filter_by(company_id=current_user.company_id).count()
    
    # Get today's attendance count
    today = date.today()
    today_attendance = Attendance.query.filter_by(
        company_id=current_user.company_id,
        work_date=today
    ).count()
    
    # Get today's total wages
    today_records = Attendance.query.filter_by(
        company_id=current_user.company_id,
        work_date=today
    ).all()
    today_wages = sum(float(r.wage_amount) for r in today_records)
    
    # Get recent attendance records (last 10)
    recent_attendance = (
        Attendance.query
        .filter_by(company_id=current_user.company_id)
        .join(Labor)
        .add_entity(Labor)
        .order_by(Attendance.work_date.desc(), Attendance.id.desc())
        .limit(10)
        .all()
    )
    
    return render_template(
        "dashboard.html",
        total_workers=total_workers,
        today_attendance=today_attendance,
        today_wages=today_wages,
        recent_attendance=recent_attendance,
    )
