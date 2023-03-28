from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.schema import ForeignKey
from flask_login import UserMixin

db = SQLAlchemy()


class FlightModel(db.Model):
    __tablename__ = 'flight'

    flight_number = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source = db.Column(db.String(40), ForeignKey('users.airport', ondelete='CASCADE'))
    departure = db.Column(db.DateTime, nullable=False)
    destination = db.Column(db.String(40), nullable=False)
    arrival = db.Column(db.DateTime, nullable=False)
    airline = db.Column(db.String(40), nullable=False)
    halt_station = db.Column(db.String(40), nullable=False)
    halt_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.DateTime, nullable=False, default=arrival - departure)
    delay_time = db.Column(db.DateTime, nullable=False)


class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    airport = db.Column(db.String(40), nullable=False, unique=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    email_id = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20),default='admin')
