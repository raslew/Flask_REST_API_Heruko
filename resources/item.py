
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

#för varje ny "endpoint" skapar man upp en resurs som ärver från "Resource"
class Item(Resource):
    #Gör så att reqparse tillhör Item-klassen istället för metoden så kallar du på 'Item.parser' i metoden.
    #json-payloaden kommer köras igenom reqparse och att tolka innehållet
    parser = reqparse.RequestParser()
    #lägger till argument som skall hjälpa parsern att tolka payloaden
    parser.add_argument('price',
        #kommer tolkas som en float
        type=float,
        #kräver att det finns ett pris
        required=True,
        help="This field cannot be left blank!"
        #Finns fler användabara argument att utforska
    )
    parser.add_argument('store_id',
        #kommer tolkas som en float
        type=int,
        #kräver att det finns ett pris
        required=True,
        help="Every item needs a store id"
        #Finns fler användabara argument att utforska
    )
    #@jwt_required lägg som decorator som tar in authenticate och identity. Dessa måste returerna förväntade värden för att get/post skall kunna köras.
    #Använd denna decorator för varje metod för så klienten måste identifiera sig inför varje request
    #POSTMAN info: POST/auth, Body{"username": "användare","password": "lösen"}, kopiera acces_token
    #POSTMAN info: typ av request, Header: Authentication, "JTW 'acces_token'"
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item was not found"}, 404

    #@jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            #Om item redan existerar, returnera 400 = bad request.
            return {'item': "Item with name '{}' already exists".format(name)}, 400
        #force=True även om content-type Header inte är satt till t.ex application.json så formateras den ändå.
        #silence=True returnerar ingen Error, endast None.
        #Här parsar/tolkar parse_args innehåller i parser och placerar de godkända argumenten i data

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        #samma som ovan
        #item =  ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            #500 = internal service error
            return {"message": "An error occurred while inserting the item."}, 500

        return item.json(), 201

    #@jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    #@jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)


        if item is None:
            #Om inte item finns skapas ett nytt item upp med samma namn
            item = ItemModel(name, **data)
            #samma som ovan
            #item = ItemModel(name, data['price'], data['store_id'])
        else:
            #uppdatera priset
            item.price = data['price']

        item.save_to_db()
        return item.json()

class ItemList(Resource):
    #@jwt_required()
    def get(self):
        #loopar igenom alla "item" i databasen och gör om den till ett jsonformat
        return {'items': [item.json() for item in ItemModel.query.all()]}
        #Om man vill använda lambda...
        #map använder lambda funktionen och applicerar den på varje element i "ItemModel"
        #return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
