# labor.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Labor

labor_bp = Blueprint("labor", __name__, template_folder="templates")


@labor_bp.route("/register", methods=["GET", "POST"])
def register_labor():
    if request.method == "POST":
        name = request.form.get("name")
        id_no = request.form.get("id_no")
        phone_no = request.form.get("phone_no")

        if not name or not id_no or not phone_no:
            flash("All fields are required.", "danger")
            return redirect(url_for("labor.register_labor"))

        # Check if ID already exists
        existing = Labor.query.filter_by(id_no=id_no).first()
        if existing:
            flash("Labor with this ID already exists.", "warning")
            return redirect(url_for("labor.register_labor"))

        labor = Labor(name=name, id_no=id_no, phone_no=phone_no)
        db.session.add(labor)
        db.session.commit()

        flash("Labor registered successfully!", "success")
        return redirect(url_for("labor.list_labors"))

    return render_template("labor_register.html")


@labor_bp.route("/list")
def list_labors():
    labors = Labor.query.order_by(Labor.name).all()
    return render_template("labor_list.html", labors=labors)
