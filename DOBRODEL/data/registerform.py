from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField(
        'Пароль', validators=[
            DataRequired(),
            EqualTo('repeat_password', message="Password must match")
        ]
    )
    repeat_password = PasswordField(
        'Повторите пароль',
        validators=[
            DataRequired(),
            EqualTo('password', message="Password must match")
        ]
    )
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    position = StringField('Позиция', validators=[DataRequired()])
    speciality = StringField('Вид волонтерского движения', validators=[])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
