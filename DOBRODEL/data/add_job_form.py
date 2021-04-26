from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    team_leader = IntegerField('Руководитель', validators=[DataRequired()])
    job = StringField('Дело', validators=[DataRequired()])
    work_size = IntegerField('Длительность', validators=[DataRequired()])
    collaborators = StringField('Участники', validators=[DataRequired()])
    is_finished = BooleanField('Работа завершена', default=False)

    submit = SubmitField()
