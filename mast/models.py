# ADD DB CLASSES

class Profile:
    verified = None
    email = None
    first_name = None
    last_name = None
    nickname = None
    age = None
    sex = None
    employee = None

    def __init__(self, email):
        assert(email is not None)
        self.verified = False
        self.email = email

    def verify_profile(self, first_name, last_name, age, sex, employee, nickname=None):
        assert(first_name is not None and
               last_name is not None and
               age is not None and
               sex is not None and
               employee is not None)
        self.verified = True
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.sex = sex
        self.employee = employee
        self.nickname = nickname

class UserMockup:
    def __init__(self, profile):
        self.profile = profile
