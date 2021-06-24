from flask import Flask, render_template
from pony.orm import db_session
from models import Card, User, Habilitations
from utils import affect_card, AffectError

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello world!"


@app.route("/check/<card_id>")
@db_session
def check(card_id: int):
    card = Card.get(id=card_id)
    if card is None:
        return {"found": False}
    else:
        user = card.user
        if Habilitations.get(name="Gestion Administrative") in user.habilitations:
            granted = True
        else:
            granted = False

        return {
            "found": True,
            "granted": granted,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "habs": [hab.name for hab in user.habilitations],
        }
        # return bottle.template("result.json", found='true', user=user)


@app.route("/affect/<card_id>/to_user/<user_id>")
@db_session
def affect(card_id: int, user_id: int):
    try:
        if affect_card(card_id, user_id):
            return {"success": True}
    except AffectError as e:
        return {"success": False, "message": str(e)}


@app.route("/cards")
@db_session
def list_cards():
    cards = Card.select()
    # return bottle.template("cards_listing", cards=cards)
    return {"cards": cards}


@app.route("/habs")
@db_session
def list_habs():
    habs = Habilitations.select()
    return {"habs": habs}


@app.route("/users")
@db_session
def list_users():
    users = User.select()
    # return bottle.template("users_listing", users=users)
    return render_template("users_listing.html", users=users)
