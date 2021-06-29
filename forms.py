from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.fields.core import BooleanField
from wtforms.fields.simple import SubmitField, TextField
from wtforms.validators import DataRequired, ValidationError
from models import Habilitation, User


class AffectationForm(FlaskForm):
    card_id = IntegerField("Numéro de la carte", validators=[DataRequired()])
    submit = SubmitField("Affecter")

    def validate_card_id(form, field):
        if User.exists(card=field.data):
            raise ValidationError("Cette carte est déjà affectée...")


class RoomModificationBase(FlaskForm):
    submit = SubmitField("Mettre à jour")
    name = TextField()


def room_form_builder(*args):
    class RoomModification(RoomModificationBase):
        pass

    for hab in Habilitation.select():
        setattr(RoomModification, hab.name, BooleanField())

    return RoomModification(*args)
