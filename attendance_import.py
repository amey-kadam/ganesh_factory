# attendance_import.py
import csv
import io
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Labor, Attendance

attendance_import_bp = Blueprint("attendance_import", __name__, template_folder="templates")


@attendance_import_bp.route("/", methods=["GET", "POST"])
@login_required
def import_attendance():
    """
    Upload a CSV file and import attendance.
    CSV expected columns:
      id_no, work_date (YYYY-MM-DD), labor_type, wage_amount,
      hours_worked (optional), tasks_done (optional)
    """
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            flash("Please upload a CSV file.", "danger")
            return redirect(url_for("attendance_import.import_attendance"))

        try:
            data = file.read().decode("utf-8")
        except UnicodeDecodeError:
            flash("Could not decode file. Make sure it is a UTF-8 CSV.", "danger")
            return redirect(url_for("attendance_import.import_attendance"))

        reader = csv.DictReader(io.StringIO(data))
        imported_count = 0
        skipped_count = 0

        for row in reader:
            id_no = (row.get("id_no") or "").strip()
            work_date_str = (row.get("work_date") or "").strip()
            labor_type = (row.get("labor_type") or "").strip()
            wage_amount_str = (row.get("wage_amount") or "").strip()
            hours_worked_str = (row.get("hours_worked") or "").strip()
            tasks_done_str = (row.get("tasks_done") or "").strip()

            if not (id_no and work_date_str and labor_type and wage_amount_str):
                skipped_count += 1
                continue

            labor = Labor.query.filter_by(
                id_no=id_no,
                company_id=current_user.company_id
            ).first()

            if not labor:
                skipped_count += 1
                continue

            try:
                work_date = datetime.strptime(work_date_str, "%Y-%m-%d").date()
                wage_amount = float(wage_amount_str)
            except ValueError:
                skipped_count += 1
                continue

            hours_worked = None
            if hours_worked_str:
                try:
                    hours_worked = float(hours_worked_str)
                except ValueError:
                    hours_worked = None

            tasks_done = None
            if tasks_done_str:
                try:
                    tasks_done = int(tasks_done_str)
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
            imported_count += 1

        db.session.commit()
        flash(f"Imported {imported_count} records, skipped {skipped_count}.", "success")
        return redirect(url_for("attendance_import.import_attendance"))

    # GET: show upload form
    return render_template("attendance_import.html")
