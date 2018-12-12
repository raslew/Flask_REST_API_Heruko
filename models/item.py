from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    #För att välja antalet decimaler använd "precision"
    price = db.Column(db.Float(precision=2))

    #Skapar upp en tabel i databasen som man kopplar items till
    #db.interger skall matacha med "id" under Store
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    #skapar en relation store_id och StoreModel
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}


    @classmethod
    def find_by_name(cls, name):
        #query kommer från SQLAlchemy som vi enkelt bygger querys med.
        #return ItemModel.query.filter_by(name=name) #SELECT * FROM items WHERE name=name
        #return ItemModel.query.filter_by(name=name).filter_by(id=1) #filterar på flera värden
        #return ItemModel.query.filter_by(name=name, id=1) #filterar på flera argument
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1, returnerar den första raden.


    def save_to_db(self):
        #Session är alla objekt i denna sessionen som vi skall skriva till databasen
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
