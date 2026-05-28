# controllers/auth_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import UserRepo, User  # Или from models.user import UserRepo, User, если отдельный файл

bp = Blueprint("auth", __name__, url_prefix="/auth")

repo = UserRepo()

@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("books.list_books")) # Если уже logged in, редирект на protected page

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = repo.get_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("books.list_books"))

        flash("Login successful!", "success")
    return render_template("auth/login.html") # Создайте аналогичный шаблон для регистрации


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

