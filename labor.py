# labor.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Labor, WorkerType

labor_bp = Blueprint("labor", __name__, template_folder="templates")


@labor_bp.route("/register", methods=["GET", "POST"])
@login_required
def register_labor():
    worker_types = WorkerType.query.filter_by(company_id=current_user.company_id).all()

    if request.method == "POST":
        name = request.form.get("name")
        id_no = request.form.get("id_no")
        phone_no = request.form.get("phone_no")
        worker_type_id = request.form.get("worker_type_id") or None

        if not name or not id_no or not phone_no:
            flash("All fields are required.", "danger")
            return redirect(url_for("labor.register_labor"))

        existing = Labor.query.filter_by(
            id_no=id_no,
            company_id=current_user.company_id
        ).first()
        if existing:
            flash("Labor with this ID already exists in your company.", "warning")
            return redirect(url_for("labor.register_labor"))

        labor = Labor(
            name=name,
            id_no=id_no,
            phone_no=phone_no,
            company_id=current_user.company_id,
            worker_type_id=worker_type_id,
        )
        db.session.add(labor)
        db.session.commit()

        flash("Labor registered successfully!", "success")
        return redirect(url_for("labor.list_labors"))

    return render_template("labor_register.html", worker_types=worker_types)


@labor_bp.route("/list")
@login_required
def list_labors():
    labors = Labor.query.filter_by(
        company_id=current_user.company_id
    ).order_by(Labor.name).all()
    return render_template("labor_list.html", labors=labors)
