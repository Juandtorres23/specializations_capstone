from myproject import db, login_manager, app, connect_to_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(64), unique = True, index = True, nullable = False)
    username = db.Column(db.String(64), unique = True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)
    phone = db.Column(db.String, nullable = False)
    
    pet = db.relationship("Pet", backref = "users", uselist = False)
    services = db.relationship("Service", backref = "users", uselist = False)


    def get_pets(self):
        return Pet.query.filter_by(user_id=self.id).all()

    def get_services(self):
        return Service.query.filter_by(user_id=self.id).all()
        
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

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), nullable = False)
    pet_type = db.Column(db.String(255), nullable = False)
    size = db.Column(db.String(255), nullable = False)
    weight = db.Column(db.Float, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    service = db.relationship("Service", cascade="delete", backref = "pet", lazy = 'dynamic')

    def get_services(self):
        return Service.query.filter_by(pet_id=self.id).all()

    def __init__(self, name, pet_type, size, weight, user_id):
        self.name = name
        self.pet_type = pet_type
        self.size = size
        self.weight = weight
        self.user_id = user_id

    def __repr__(self):
        return f"{self.name} a {self.pet_type} was added!"

class Service(db.Model):

    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    type_service = db.Column(db.String(255), nullable = False)
    date = db.Column(db.Date, nullable = False)
    time = db.Column(db.Time, nullable = False)
    notes = db.Column(db.String(1000))

    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'))
    pet_name = db.Column(db.String(255), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def __init__(self, type_service, date, time, notes, pet_id, pet_name, user_id):
        self.type_service = type_service
        self.date = date
        self.time = time
        self.notes = notes
        self.pet_id = pet_id
        self.pet_name = pet_name
        self.user_id = user_id

    def __repr__(self):
        return f"A {self.type_service} appointment was just created!"

if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True)  