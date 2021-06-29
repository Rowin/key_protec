from flask import Flask, render_template, abort, request, redirect
from flask.helpers import flash, url_for
from pony.orm import db_session
from models import Room, User, Habilitation
from forms import AffectationForm, room_form_builder

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
    habs = Habilitation.select()
    return render_template("habs_listing.html", habs=habs)


@app.route("/users")
@db_session
def list_users():
    users = User.select()
    form: AffectationForm = AffectationForm(request.form)
    return render_template("users_listing.html", users=users, form=form)


@app.route("/rooms")
@db_session
def list_rooms():
    rooms = Room.select()
    habilitations = Habilitation.select()
    form = room_form_builder()
    return render_template(
        "room_listing.html", rooms=rooms, habilitations=habilitations, form=form
    )


@app.route("/room/<int:room_id>/update", methods=["POST"])
@db_session
def update_room(room_id):
    room: Room = Room.get(id=room_id)

    if room is None:
        abort(404)

    form = room_form_builder(request.form)
    if form.validate():
        room.name = form.name.data

        hab_set = list()
        for hab in Habilitation.select():
            if form[hab.name].data:
                hab_set.append(hab)
        room.habilitations = hab_set
        flash("Pièce mise à jour", "success")

    return redirect(url_for("list_rooms"))


@app.route("/room/create")
def create_room():
    pass
