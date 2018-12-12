from flask_sqlalchemy import SQLAlchemy

#SQLAlchemy kommer att länka till flaskappen och kommer titta på alla objekten som vi tillåter den till och mappa upp dessa objekt till rader i vår databas
#T.ex. när vi skapar en item.model-objekt som har kolumner med namn och pris så kommer den ta objektet och placera det i databasen
db = SQLAlchemy()
