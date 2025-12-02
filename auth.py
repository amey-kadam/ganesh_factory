# auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User, Company

auth_bp = Blueprint("auth", __name__, template_folder="templates")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Register a new company + admin user.
    """
    if request.method == "POST":
        company_name = request.form.get("company_name")
        company_address = request.form.get("company_address")
        company_phone = request.form.get("company_phone")

        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not (company_name and email and password and confirm_password):
            flash("All required fields must be filled.", "danger")
            return redirect(url_for("auth.register"))

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("User with this email already exists.", "warning")
            return redirect(url_for("auth.register"))

        existing_company = Company.query.filter_by(name=company_name).first()
        if existing_company:
            flash("Company with this name already exists.", "warning")
            return redirect(url_for("auth.register"))

        company = Company(
            name=company_name,
            address=company_address,
            phone=company_phone,
        )
        db.session.add(company)
        db.session.flush()  # get company.id

        user = User(
            email=email,
            password_hash=generate_password_hash(password),
            role="admin",
            company_id=company.id,
        )
        db.session.add(user)
        db.session.commit()

        flash("Company and admin user registered. Please log in.", "success")
        return redirect(url_for("auth.login"))

    # GET
    return render_template("auth_register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid email or password.", "danger")
            return redirect(url_for("auth.login"))

        login_user(user)
        flash("Logged in successfully.", "success")
        # redirect to dashboard
        return redirect(url_for("main.dashboard"))

    return render_template("auth_login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    """
    Very basic placeholder:
    - You can implement real email-based reset later.
    """
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("If this email exists, password reset instructions will be sent.", "info")
        else:
            # Here you would normally generate a token and send an email.
            # For now, just show a message.
            flash("Password reset feature is not fully implemented yet.", "info")
        return redirect(url_for("auth.login"))

    return render_template("auth_forgot_password.html")
