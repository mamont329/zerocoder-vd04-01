# zerocoder-vd04-01 — Flask: шесть задач по нарастающей

Работы блока веб-разработки на Flask — от минимального приложения до полноценной аутентификации.

| Папка | Что реализовано |
|---|---|
| `task1` | Минимальное приложение с шаблоном (текущие дата и время) |
| `task2` | Многостраничный сайт: статика, CSS, несколько шаблонов |
| `task3` | Наследование шаблонов Jinja2 через `base.html` |
| `task4` | Рефакторинг в пакет `app/` (`__init__.py`, `routes.py`), форма-анкета |
| `task5` | **Полноценная авторизация**: модель `User` с `UserMixin`, регистрация / вход / выход, **bcrypt-хеширование паролей**, WTForms-валидация (`Email`, `EqualTo`, кастомные `ValidationError`), редактирование профиля, смена пароля; `create_db.py` для инициализации БД |
| `task6` | Работа с внешним API — страница случайных цитат |

Стек: Flask, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt, Flask-WTF/WTForms, Jinja2, SQLite.

## Запуск (на примере task5)

```bash
python -m venv .venv && .venv\Scripts\activate   # Windows
pip install flask flask-sqlalchemy flask-login flask-bcrypt flask-wtf email-validator requests
cd task5
python create_db.py
python main.py
```

`task1`–`task3` запускаются как `python app.py` из своей папки, `task4` и `task6` — как `python main.py`.

Продолжение этой линии — кликер с регистрацией и авторизацией, задеплоенный на PythonAnywhere: https://mamont329.pythonanywhere.com/

---
Учебная работа курса Университета Зерокодинга «Программист на Python с нуля с помощью ChatGPT» (2026), блок «Веб-разработка на Flask».
