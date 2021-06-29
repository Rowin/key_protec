from pony.orm import Database, Required, PrimaryKey, Set, Optional

db = Database()


# class Card(db.Entity):
#     id = PrimaryKey(int, auto=False)
#     user = Optional("User")


class User(db.Entity):
    id = PrimaryKey(int, auto=False)
    lastname = Required(str)
    firstname = Required(str)
    card = Optional(int, unique=True)
    habilitations = Set("Habilitation")

    def __next__(self):
        pass

    def __iter__(self):
        pass

    def __repr__(self):
        return f"<{self.firstname} {self.lastname}>"


class Habilitation(db.Entity):
    name = Required(str)
    users = Set("User")
    rooms = Set("Room")


class Room(db.Entity):
    name = Required(str)
    habilitations = Set("Habilitation")


db.bind(provider="sqlite", filename="database.sqlite", create_db=True)
db.generate_mapping(create_tables=False)
