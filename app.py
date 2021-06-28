from flask import Flask, render_template, abort, request, redirect
from flask.helpers import flash, url_for
from pony.orm import db_session
from models import User, Habilitations
from forms import AffectationForm

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
def index():
    return "Hello world!"


@app.route("/users/<int:user_id>/affect", methods=["POST"])
@db_session
def affect(user_id: int):
    user: User = User.get(id=user_id)
    if user is None:
        abort(404)

    form: AffectationForm = AffectationForm(request.form)
    if request.method == "POST" and form.validate():
        user.card = form.card_id.data
        flash("Carte mise à jour", "success")

    return redirect(url_for("list_users"))


@app.route("/users/<int:user_id>/deaffect", methods=["GET"])
@db_session
def deaffect(user_id: int):
    user: User = User.get(id=user_id)
    if user is None:
        abort(404)

    user.card = None
    flash("Carte désaffectée avec succès", "success")
    return redirect(url_for("list_users"))


# @app.route("/cards")
# @db_session
# def list_cards():
#     cards = Card.select()
#     return render_template("cards_listing.html", cards=cards)


@app.route("/habs")
@db_session
def list_habs():
    habs = Habilitations.select()
    return render_template("habs_listing.html", habs=habs)


@app.route("/users")
@db_session
def list_users():
    users = User.select()
    form: AffectationForm = AffectationForm(request.form)
    return render_template("users_listing.html", users=users, form=form)
