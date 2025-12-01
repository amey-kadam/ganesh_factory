# admin_panel.py
from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Labor, Attendance

admin_bp = Blueprint("admin", __name__, template_folder="templates")


@admin_bp.route("/attendance", methods=["GET", "POST"])
def mark_attendance():
    labors = Labor.query.order_by(Labor.name).all()

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

        try:
            work_date = datetime.strptime(work_date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format.", "danger")
            return redirect(url_for("admin.mark_attendance"))

        # Convert numbers
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
            labor_id=labor_id,
            work_date=work_date,
            labor_type=labor_type,
            wage_amount=wage_amount,
            hours_worked=hours_worked,
            tasks_done=tasks_done,
        )

        db.session.add(attendance)
        db.session.commit()

        flash("Attendance saved successfully.", "success")
        return redirect(url_for("admin.today_attendance"))

    # GET – show form
    today_str = date.today().strftime("%Y-%m-%d")
    return render_template(
        "admin_attendance.html",
        labors=labors,
        today_str=today_str,
    )


@admin_bp.route("/attendance/today")
def today_attendance():
    today = date.today()
    records = (
        Attendance.query.filter_by(work_date=today)
        .join(Labor)
        .add_entity(Labor)
        .all()
    )
    return render_template(
        "admin_attendance_today.html",
        records=records,
        report_date=today
    )
