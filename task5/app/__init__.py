"""Создание приложения и подключение расширений.

Здесь рождается объект app и все расширения (БД, хеширование, вход).
Маршруты импортируем в конце — когда app уже готов.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

# SECRET_KEY нужен для сессий и защиты форм (CSRF). В реальном проекте
# он секретный и хранится вне кода; у нас учебный — заглушка.
app.config["SECRET_KEY"] = "uchebnyy-secret-key-task5"
# Файл базы данных SQLite. По умолчанию ляжет в папку instance/.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)          # база данных (ORM)
bcrypt = Bcrypt(app)          # хеширование паролей
login_manager = LoginManager(app)   # управление входом
# Куда перенаправлять, если незалогиненный лезет на защищённую страницу.
login_manager.login_view = "login"
login_manager.login_message = "Пожалуйста, войдите, чтобы открыть эту страницу."

from app import routes  # noqa: E402  (в конце — так и задумано)
