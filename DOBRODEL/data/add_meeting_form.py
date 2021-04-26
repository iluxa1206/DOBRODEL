from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class AddMeetingForm(FlaskForm):
    tema = StringField('Тема cобрания', validators=[DataRequired()])
    leader = IntegerField('Глава cобрания', validators=[DataRequired()])
    members = StringField('Участники', validators=[DataRequired()])
    email = EmailField(validators=[DataRequired()])
    submit = SubmitField('Добавить')
