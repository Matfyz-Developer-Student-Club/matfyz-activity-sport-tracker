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
