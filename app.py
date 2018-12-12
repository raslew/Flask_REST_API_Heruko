from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
#När vi använder flask_restful behöver vi inte använda jsonify. Det fixat flask_restful åt oss.

app = Flask(__name__)
#"SQLAlchemy databas" kommer finnas i rotenkatalogen av projekt
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'rasmus'
api = Api(app)

#JWT skapar en ny endpoint /auth
#När vi kallar på /auth skickar vi username och password som vidarebefodrar de till authenticate-funktionen som returnerar en JWT-Token.
#Vid nästa request så använder vi vår JTW-Token och skickar med till identity-funktionen som kan returnera om usern finns och returnerar "user_id" och JWT-token är valid
jwt = JWT(app, authenticate, identity)

#Förklarar vilken endpoint och klass som hör ihop.
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
#debug=True ger dig en html-sida där du kan fel söka när något är fel i koden.
#flask använder port 5000
#förhindrar att "app.run" körs ifall man vill importera "app.py" i en annan fil den körs.

if __name__ == '__main__':
    #importeras här pga circular import
    from db import db
    db.init_app(app)
    app.run(port=5000)
