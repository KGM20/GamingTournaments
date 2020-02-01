
from sqlalchemy import Column, String, Integer, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Player
A person interested to play games tournaments
'''
class Player(db.Model):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    nationality = Column(String)

    def __init__(self, name, nickname, nationality):
        self.name = name
        self.nickname = nickname
        self.nationality = nationality

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'nickname': self.nickname,
            'nationality': self.nationality
        }


'''
Game
A game :)
'''
class Game(db.Model):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    def __init__(self, title):
        self.title = title

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title
        }

'''
A many to many relationship between players and tourneys
'''
players_tourneys = db.Table('players_tourneys',
    Column('player_id', Integer, db.ForeignKey('players.id'), primary_key=True),
    Column('tourney_id', Integer, db.ForeignKey('tourneys.id'), primary_key=True)
)

'''
Tourney
An events where players gather to play against each other to see who's the best
'''
class Tourney(db.Model):
    __tablename__ = 'tourneys'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    winner = Column(Integer, db.ForeignKey('players.id'))
    game_id = Column(Integer, db.ForeignKey('games.id'), nullable=False)
    players = db.relationship('Player', secondary=players_tourneys,
		backref=db.backref('player_tourneys', lazy=True))

    def __init__(self, name, location, date, game_id):
        self.name = name
        self.location = location
        self.date = date
        self.winner = None
        self.game_id = game_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'date': self.date,
        	'winner': self.winner,
        	'game_id': self.game_id
        }
