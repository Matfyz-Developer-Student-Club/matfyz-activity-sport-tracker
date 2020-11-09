from mast import db, login_manager
from flask_login import UserMixin
from enum import Enum


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class Sex(Enum):
    Male = 1
    Female = 2

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Age(Enum):
    Under35 = 1
    Over35 = 2

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class UserType(Enum):
    Student = 1
    Employee = 2
    Alumni = 3

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class ActivityType(Enum):
    Walk = 1
    Run = 2
    Ride = 3

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Competition(Enum):
    Run5km = 5
    Run10km = 10

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    first_name = db.Column(db.String(20), nullable=False, default='')
    last_name = db.Column(db.String(50), nullable=False, default='')
    display_name = db.Column(db.String(50))
    sex = db.Column(db.Enum(Sex))
    age = db.Column(db.Enum(Age))
    anonymous = db.Column(db.Boolean, nullable=False, default=False)
    type = db.Column(db.Enum(UserType))
    uk_id = db.Column(db.String(10))
    verified = db.Column(db.Boolean, nullable=False, default=False)
    shirt_size = db.Column(db.String(100))
    competing = db.Column(db.Boolean, nullable=False, default=True)
    activities = db.relationship('Activity', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.email}')"

    def __init__(self, email, password):
        assert (email is not None and
                password is not None)
        self.email = email
        self.password = password
        db.session.add(self)
        db.session.commit()

    def complete_profile(self, first_name, last_name, age, sex, shirt_size, user_type, ukco, anonymous,
                         display_name=None):
        assert (first_name is not None and
                last_name is not None and
                age is not None and
                sex is not None and
                shirt_size is not None and
                user_type is not None and
                ukco is not None)
        self.first_name = first_name
        self.last_name = last_name
        if age == '<=35':
            self.age = Age.Under35
        else:
            self.age = Age.Over35
        if sex == 'male':
            self.sex = Sex.Male
        else:
            self.sex = Sex.Female
        self.shirt_size = shirt_size
        if user_type == 'student':
            self.type = UserType.Student
        elif user_type == 'employee':
            self.type = UserType.Employee
        else:
            self.type = UserType.Alumni
        self.uk_id = ukco
        self.anonymous = anonymous
        self.display_name = display_name
        db.session.add(self)
        db.session.commit()

    def verify(self):
        self.verified = True
        db.session.add(self)
        db.session.commit()

    def change_password(self, password):
        assert (password is not None)
        self.password = password
        db.session.add(self)
        db.session.commit()


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
