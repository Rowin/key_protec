from pony.orm import db_session
from pony.orm.core import ObjectNotFound

from models import Card, User


class AffectError(Exception):
    pass


@db_session
def affect_card(card_id, eprotec_id):
    user = User.get(id=eprotec_id)
    if user is None:
        raise AffectError("User not found")
    else:
        if Card.exists(id=card_id):
            Card[card_id].set(user=user)
        else:
            Card(id=card_id, user=user)

        return True


@db_session
def get_eprotec_id(card_id):
    try:
        return Card[card_id].eprotec_id
    except ObjectNotFound:
        return False
