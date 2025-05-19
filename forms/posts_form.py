from html.entities import html5

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, NumberRange


class PostForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    hard = IntegerField('Сложность', validators=[DataRequired(), NumberRange(min=1, max=10)] )
    text = StringField('Условие задачи', validators=[DataRequired()])
    decision = TextAreaField('Решение задачи', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')

