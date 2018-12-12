#importerar sqlite3 så att klassen kan interagera med sqlite3
import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field is mandatory"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field is mandatory"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        #Om påståendet är sant. Dvs om data['username'] redan finns i databasen.
        #Returnera att det användarnamnet redan finns.
        #Denna checken skall ligga innan connection annars kommer den aldrig stängas.
        if UserModel.find_by_username(data['username']):
            return {"message": "Username already exists. Choose another"}, 400

        #**data = for each key in "data"
        #**data är en dict och därav tar ** första key och dess value och placerar i username,
        #därefter behandlas nästa key och value på samma sätt och placeras i password
        #Pga vi använder en parser så vet du att värderna i data överensstämmer med vad vi behöver.
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User successfully created!"}, 201
