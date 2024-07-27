from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectMultipleField
from wtforms.validators import DataRequired

class FirstMethodForm(FlaskForm):
    azs = SelectMultipleField('Выберите НПЗ', choices=[], validators=[DataRequired()])
    submit = SubmitField('Отправить')

    def set_choices(self, azs_list):
        self.azs.choices = [(azs, azs) for azs in azs_list]