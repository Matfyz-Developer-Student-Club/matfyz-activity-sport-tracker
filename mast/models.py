from mast import db, login_manager
from flask_login import UserMixin
import enum


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Sex(enum.Enum):
    Male = 1
    Female = 2


class Age(enum.Enum):
    Under35 = 1
    Over35 = 2


class ActivityType(enum.Enum):
    Walk = 1
    Run = 2
    Ride = 3


class Competition(enum.Enum):
    Run5km = 1
    Run10km = 2


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    sex = db.Column(db.Enum(Sex))
    age = db.Column(db.Enum(Age))
    nick_name = db.Column(db.String(50))
    anonymous = db.Column(db.Boolean)
    uk_id = db.Column(db.String(10))
    validated = db.Column(db.Boolean, nullable=False)
    activities = db.relationship('Activity', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', {self.name} {self.surname}, {self.sex.name} {self.age.name})"


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Time, nullable=False)
    type = db.Column(db.Enum(ActivityType), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    competition = db.Column(db.Enum(Competition))

    def __repr__(self):
        return f"Activity({self.date}: {self.type.name} {self.distance} km, time: {self.duration})"
