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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime = db.Column(db.DateTime, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Time, nullable=False)
    average_duration_per_km = db.Column(db.Time, nullable=False)
    type = db.Column(db.Enum(ActivityType), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Activity({self.datetime}: {self.type.name} {self.distance} km, time: {self.duration})"


class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    challenge_parts = db.relationship('ChallengePart', order_by='ChallengePart.order', backref='season', lazy=True)

    def __repr__(self):
        return f"Activity({self.title}: {self.start_date} - {self.end_date})"


class ChallengePart(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    target = db.Column(db.String(100), nullable=False)
    distance = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"ChallengePart(#{self.order}: to {self.target} {self.distance} km)"

# ADD DB CLASSES

class Profile:
    verified = None
    email = None
    first_name = None
    last_name = None
    display_name = None
    age = None
    sex = None
    shirt_size = None
    employee = None
    competing = None

    def __init__(self, email):
        assert(email is not None)
        self.verified = False
        self.email = email

    def complete_profile(self, first_name, last_name, age, sex, shirt_size, employee, competing, display_name=None):
        assert(first_name is not None and
               last_name is not None and
               age is not None and
               sex is not None and
               shirt_size is not None and
               employee is not None and
               competing is not None)
        self.verified = True
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.sex = sex
        self.shirt_size = shirt_size
        self.employee = employee
        self.competing = competing
        self.display_name = display_name

class UserMockup:
    def __init__(self, profile):
        self.profile = profile
