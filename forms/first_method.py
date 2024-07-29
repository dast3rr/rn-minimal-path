from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired

class FirstMethodForm(FlaskForm):
    npz = SelectField('Выберите НПЗ', choices=[], validators=[DataRequired()])
    azs = SelectMultipleField('Выберите АЗС', choices=[], validators=[DataRequired()])
    submit = SubmitField('Рассчитать')

    def set_azs_choices(self, azs_list):
        self.azs.choices = [(azs, azs) for azs in azs_list]

    def set_npz_choices(self, npz_list):
        self.npz.choices = [(npz, npz) for npz in npz_list]