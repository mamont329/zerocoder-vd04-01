"""Создание таблиц базы данных.

Запусти ОДИН раз перед первым стартом:  python create_db.py
Создаст файл instance/site.db с таблицей users.
"""
from app import app, db
from app.models import User  # noqa: F401  (нужен, чтобы db знал о модели)

with app.app_context():
    db.create_all()
    print("База данных создана (instance/site.db).")
