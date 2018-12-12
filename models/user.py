import sqlite3
from db import db

#Extend db.Model så skapar man en länk mellan classen och databasen
class UserModel(db.Model):
     #Talar om för SQLAlchemy i vilken tabellnamn UserModel skall sparas
    __tablename__ = 'users'

    #Talar om för SQLAlchemy i vilken kolumn User skall sparas
    #Variabelnamnen måste vara samma som klassens variabler för att kunna sparas till databasenself.
    #id() är en inbyggd funktion i python som returnerar en interger som är unik
    id = db.Column(db.Integer, primary_key=True)
    #Bra att ha en limit på hur många tecken användaren får ha. I detta fallet 80 tecken.
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))


    def __init__(self, username, password):
        self.username = username
        self.password = password

    #pga vi använder User i metoden så byter vi ut self och User mot cls och lägger till @classmethod
    #Detta görs pga vi inte skall hårdkoda in User ifall vi skall ändra på klassen i framtiden.
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
