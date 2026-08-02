"""Точка запуска приложения.

Берём готовый объект app из пакета app/ и запускаем сервер.
Запуск:  python main.py
"""
from app import app

if __name__ == "__main__":
    app.run(debug=True)
