from mast import db, login_manager
from flask_login import UserMixin
from enum import Enum


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class Sex(Enum):
    Male = 1
    Female = 2


class Age(Enum):
    Under35 = 1
    Over35 = 2


class UserType(Enum):
    Student = 1
    Employee = 2
    Alumni = 3


class ActivityType(Enum):
    Walk = 1
    Run = 2
    Ride = 3


class Competition(Enum):
    Run5km = 5
    Run10km = 10


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    display_name = db.Column(db.String(50))
    sex = db.Column(db.Enum(Sex))
    age = db.Column(db.Enum(Age))
    anonymous = db.Column(db.Boolean, nullable=False, default=False)
    type = db.Column(db.Enum(UserType))
    uk_id = db.Column(db.String(10))
    validated = db.Column(db.Boolean, nullable=False, default=False)
    t_shirt = db.Column(db.String(100))
    competing = db.Column(db.Boolean, nullable=False, default=True)
    activities = db.relationship('Activity', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.display_name}', {self.name} {self.surname}, {self.sex.name} {self.age.name})"


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Time, nullable=False)
    average_duration_per_km = db.Column(db.Time, nullable=False)
    type = db.Column(db.Enum(ActivityType), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Activity({self.datetime}: {self.type.name} {self.distance} km, time: {self.duration})"
