# admin_panel.py
from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Labor, Attendance

admin_bp = Blueprint("admin", __name__, template_folder="templates")


@admin_bp.route("/attendance", methods=["GET", "POST"])
@login_required
def mark_attendance():
    labors = Labor.query.filter_by(
        company_id=current_user.company_id
    ).order_by(Labor.name).all()

    if request.method == "POST":
        labor_id = request.form.get("labor_id")
        work_date_str = request.form.get("work_date")
        labor_type = request.form.get("labor_type")
        wage_amount = request.form.get("wage_amount")
        hours_worked = request.form.get("hours_worked") or None
        tasks_done = request.form.get("tasks_done") or None

        if not (labor_id and work_date_str and labor_type and wage_amount):
            flash("Labor, date, type and wage are required.", "danger")
            return redirect(url_for("admin.mark_attendance"))

        # Ensure labor belongs to current company
        labor = Labor.query.filter_by(
            id=labor_id,
            company_id=current_user.company_id
        ).first()
        if not labor:
            flash("Invalid labor selected.", "danger")
            return redirect(url_for("admin.mark_attendance"))

        try:
            work_date = datetime.strptime(work_date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format.", "danger")
            return redirect(url_for("admin.mark_attendance"))

        try:
            wage_amount = float(wage_amount)
        except ValueError:
            flash("Wage must be a number.", "danger")
            return redirect(url_for("admin.mark_attendance"))

        if hours_worked is not None:
            try:
                hours_worked = float(hours_worked)
            except ValueError:
                hours_worked = None

        if tasks_done is not None:
            try:
                tasks_done = int(tasks_done)
            except ValueError:
                tasks_done = None

        attendance = Attendance(
            labor_id=labor.id,
            work_date=work_date,
            labor_type=labor_type,
            wage_amount=wage_amount,
            hours_worked=hours_worked,
            tasks_done=tasks_done,
            company_id=current_user.company_id,
        )

        db.session.add(attendance)
        db.session.commit()

        flash("Attendance saved successfully.", "success")
        return redirect(url_for("admin.today_attendance"))

    today_str = date.today().strftime("%Y-%m-%d")
    return render_template(
        "admin_attendance.html",
        labors=labors,
        today_str=today_str,
    )


@admin_bp.route("/attendance/today")
@login_required
def today_attendance():
    today = date.today()
    records = (
        Attendance.query
        .filter_by(work_date=today, company_id=current_user.company_id)
        .join(Labor)
        .add_entity(Labor)
        .all()
    )
    return render_template(
        "admin_attendance_today.html",
        records=records,
        report_date=today
    )
