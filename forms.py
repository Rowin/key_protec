from wtforms import Form, IntegerField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, ValidationError
from models import User


class AffectationForm(Form):
    card_id = IntegerField("Numéro de la carte", validators=[DataRequired()])
    submit = SubmitField("Affecter")

    def validate_card_id(form, field):
        if User.exists(card=field.data):
            raise ValidationError("Cette carte est déjà affectée...")
