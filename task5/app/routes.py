from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

from app import app, db, bcrypt
from app.models import User
from app.forms import RegistrationForm, LoginForm, UpdateProfileForm, ChangePasswordForm

# Список анкет — как в Задании 4, живёт в памяти (в БД не переносим).
anketas = []


# ===================== ОБЫЧНЫЙ САЙТ =====================

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", active="home")


@app.route("/about")
def about():
    return render_template("about.html", active="about")


@app.route("/anketa", methods=["GET", "POST"])
def anketa():
    if request.method == "POST":
        name = request.form.get("name")
        city = request.form.get("city")
        hobby = request.form.get("hobby")
        age = request.form.get("age")
        if name and city and hobby and age:
            anketas.append({"name": name, "city": city, "hobby": hobby, "age": age})
            return redirect(url_for("anketa"))
    return render_template("anketa.html", active="anketa", anketas=anketas)


# ===================== АУТЕНТИФИКАЦИЯ =====================

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Вы успешно зарегистрировались! Теперь войдите.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form, title="Регистрация")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Вы вошли в систему.", "success")
            return redirect(url_for("home"))
        else:
            flash("Неверная почта или пароль.", "danger")
    return render_template("login.html", form=form, title="Вход")


@app.route("/logout")
def logout():
    logout_user()
    flash("Вы вышли из системы.", "success")
    return redirect(url_for("home"))


# ===================== ЛИЧНЫЙ КАБИНЕТ =====================

@app.route("/account")
@login_required
def account():
    return render_template("account.html", active="account", title="Аккаунт")


@app.route("/account/edit", methods=["GET", "POST"])
@login_required
def edit_account():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        # Меняем поля уже существующего пользователя и коммитим — это UPDATE.
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Профиль обновлён.", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        # Предзаполняем форму текущими данными — ТОЛЬКО на GET.
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("edit_account.html", form=form, active="account", title="Редактирование профиля")


@app.route("/account/password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # Текущий пароль уже проверен в форме (validate_current_password).
        hashed = bcrypt.generate_password_hash(form.new_password.data).decode("utf-8")
        current_user.password = hashed
        db.session.commit()
        flash("Пароль изменён.", "success")
        return redirect(url_for("account"))
    return render_template("change_password.html", form=form, active="account", title="Смена пароля")
