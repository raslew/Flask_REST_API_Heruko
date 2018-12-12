from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    #För att välja antalet decimaler använd "precision"

    #skapar upp en "flera till en"-relation med ItemModel och därav en lista av "ItemModels"
    #läs på om "lazy". Har något med avvägningen av hastighet vid skapande och sökande av i tabeller
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    #.all är kopplat till "lazy=dynamic".
    def json(self):
        return {'name': self.name, 'items':[item.json() for item in self.items.all()]}


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
