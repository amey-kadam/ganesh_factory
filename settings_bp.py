# settings_bp.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Company, WorkerType

settings_bp = Blueprint("settings_bp", __name__, template_folder="templates")


@settings_bp.route("/company", methods=["GET", "POST"])
@login_required
def company_settings():
    company = current_user.company

    if request.method == "POST":
        company.name = request.form.get("name") or company.name
        company.address = request.form.get("address")
        company.phone = request.form.get("phone")
        db.session.commit()
        flash("Company settings updated.", "success")
        return redirect(url_for("settings_bp.company_settings"))

    return render_template("settings_company.html", company=company)


@settings_bp.route("/worker-types", methods=["GET", "POST"])
@login_required
def worker_types():
    company = current_user.company

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        if not name:
            flash("Worker type name is required.", "danger")
            return redirect(url_for("settings_bp.worker_types"))

        wt = WorkerType(name=name, description=description, company_id=company.id)
        db.session.add(wt)
        db.session.commit()
        flash("Worker type added.", "success")
        return redirect(url_for("settings_bp.worker_types"))

    worker_types = WorkerType.query.filter_by(company_id=company.id).all()
    return render_template("settings_worker_types.html", worker_types=worker_types)
