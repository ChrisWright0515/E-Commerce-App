from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import * 


db_url = 'mysql://root:0515@localhost/game_store'
engine = create_engine(db_url, echo=True)
conn = engine.connect()