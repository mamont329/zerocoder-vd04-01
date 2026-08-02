from flask import render_template, request, redirect, url_for

from app import app

# Список заполненных анкет. Живёт в памяти работающего сервера:
# создаётся ОДИН раз при запуске и дальше только пополняется.
# При перезапуске сервера обнуляется (базы данных пока нет).
anketas = []


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", active="home")


@app.route("/about")
def about():
    return render_template("about.html", active="about")


@app.route("/anketa", methods=["GET", "POST"])
def anketa():
    # Если пришли данные формы (нажали «Отправить») — это POST.
    if request.method == "POST":
        # Читаем поля по их name из формы (см. anketa.html).
        name = request.form.get("name")
        city = request.form.get("city")
        hobby = request.form.get("hobby")
        age = request.form.get("age")

        # Добавляем анкету только если все поля заполнены.
        if name and city and hobby and age:
            anketas.append({
                "name": name,
                "city": city,
                "hobby": hobby,
                "age": age,
            })
            # Редирект после отправки (Post/Redirect/Get):
            # браузер сделает обычный GET, и повторная отправка по F5 не сработает.
            return redirect(url_for("anketa"))

    # Обычный заход (GET) или POST без редиректа — показываем форму и список.
    return render_template("anketa.html", active="anketa", anketas=anketas)
