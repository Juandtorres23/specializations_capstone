from myproject import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincoment = True)
    email = db.Column(db.String(64), unique = True, index = True, nullable = False)
    username = db.Column(db.String(64), unique = True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)
    phone = db.Column(db.Integer, nullable = False)
    
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'))

    def __init__(self, email, username, password, phone, pet_id):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.phone = phone
        self.pet_id = pet_id

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User {self.username} was created!"

class Pet(db.Model):

    __tablename__ = "pet"

    id = db.Column(db.Integer, primary_key = True, autoincoment = True)
    name = db.Column(db.String(255), nullable = False)
    pet_type = db.Column(db.String(255), nullable = False)
    size = db.Column(db.String(255), nullable = False)
    weight = db.Column(db.float, nullable = False)

    user = db.relationship("User", backref = "pet", uselist = False)
    service = db.relationship("Service", backref = "pet", lazy = 'dynamic')

    def __init__(self, name, pet_type, size, weight):
        self.name = name
        self.pet_type = pet_type
        self.size = size
        self.weight = weight

    def __repr__(self):
        return f"{self.name} a {self.pet_type} was added!"

class Service(db.Model):

    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key = True, autoincoment = True)
    type_service = db.Column(db.String(255), nullable = False)
    date = db.Column(db.date, nullable = False)
    time = db.Column(db.time, nullable = False)
    duration = db.Column(db.time, nullable = False)
    notes = db.Column(db.String(1000))

    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'))

    def __init__(self, type_service, date, time, duration, pet_id):
        self.type_service = type_service
        self.date = date
        self.time = time
        self.duration = duration
        self.pet_id = pet_id

    def __repr__(self):
        return f"A {self.type_service} appointment was just created!"