from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

from app.models import User
from app import bcrypt

# Русские тексты для стандартных валидаторов (у WTForms они по умолчанию английские).
MSG_REQUIRED = "Заполните это поле"
MSG_EMAIL = "Введите корректный адрес почты"


class RegistrationForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[
        DataRequired(message=MSG_REQUIRED),
        Length(min=2, max=20, message="Имя должно быть от 2 до 20 символов"),
    ])
    email = StringField("Почта", validators=[
        DataRequired(message=MSG_REQUIRED),
        Email(message=MSG_EMAIL),
    ])
    password = PasswordField("Пароль", validators=[DataRequired(message=MSG_REQUIRED)])
    confirm_password = PasswordField("Повторите пароль", validators=[
        DataRequired(message=MSG_REQUIRED),
        EqualTo("password", message="Пароли должны совпадать"),
    ])
    submit = SubmitField("Зарегистрироваться")

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Такое имя уже занято")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Такая почта уже используется")


class LoginForm(FlaskForm):
    email = StringField("Почта", validators=[
        DataRequired(message=MSG_REQUIRED),
        Email(message=MSG_EMAIL),
    ])
    password = PasswordField("Пароль", validators=[DataRequired(message=MSG_REQUIRED)])
    remember = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")


class UpdateProfileForm(FlaskForm):
    """Редактирование профиля: имя и почта (без пароля)."""
    username = StringField("Имя пользователя", validators=[
        DataRequired(message=MSG_REQUIRED),
        Length(min=2, max=20, message="Имя должно быть от 2 до 20 символов"),
    ])
    email = StringField("Почта", validators=[
        DataRequired(message=MSG_REQUIRED),
        Email(message=MSG_EMAIL),
    ])
    submit = SubmitField("Сохранить")

    def validate_username(self, username):
        # Ругаемся, только если имя ИЗМЕНИЛОСЬ и уже занято кем-то другим.
        # Если оставил своё прежнее — проверку пропускаем (не спотыкаемся о себя).
        if username.data != current_user.username:
            if User.query.filter_by(username=username.data).first():
                raise ValidationError("Такое имя уже занято")

    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError("Такая почта уже используется")


class ChangePasswordForm(FlaskForm):
    """Смена пароля: текущий (для проверки) + новый + повтор."""
    current_password = PasswordField("Текущий пароль", validators=[DataRequired(message=MSG_REQUIRED)])
    new_password = PasswordField("Новый пароль", validators=[
        DataRequired(message=MSG_REQUIRED),
        Length(min=4, message="Пароль должен быть не короче 4 символов"),
    ])
    confirm_password = PasswordField("Повторите новый пароль", validators=[
        DataRequired(message=MSG_REQUIRED),
        EqualTo("new_password", message="Пароли должны совпадать"),
    ])
    submit = SubmitField("Сменить пароль")

    def validate_current_password(self, current_password):
        # Сверяем введённый текущий пароль с хешем в базе.
        if not bcrypt.check_password_hash(current_user.password, current_password.data):
            raise ValidationError("Неверный текущий пароль")
