from myproject import app, db, connect_to_db
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from myproject.model import User, Pet, Service
from myproject.forms import LoginForm, RegistrationForm, AddPetForm, AddServiceForm

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/welcome')
@login_required
def welcome_user():
    pets = current_user.get_pets()

    services = current_user.get_services()

    return render_template('profile.html', pets=pets, services=services)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out!")
    return redirect(url_for('home'))

@app.route('/login', methods = ['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):

            login_user(user)
            # need to remove one of these flashes when loging in 

            flash('Logged in Successfully!')

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('welcome_user')
            flash('You are logged in!')
            return redirect(next)
        else:
            flash('Invalid username or password')

    return render_template('login.html', form=form)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:  
            user = User(email=form.email.data,
            username=form.username.data,
            phone=form.phone.data,
            pet_id=None,
            password=form.password.data)
        
            db.session.add(user)
            db.session.commit()
            flash("Thanks for registering!")
            return redirect(url_for('login'))
        else:
            flash('Username already in use!')
    return render_template('register.html', form=form)

@app.route('/add_pet', methods = ['GET', 'POST'])
@login_required
def add_pet():
    form = AddPetForm()

    if form.validate_on_submit():
        pet = Pet(name=form.name.data,
                    pet_type=form.pet_type.data,
                    size=form.size.data,
                    weight=form.weight.data,
                    user_id=current_user.id)

        db.session.add(pet)
        db.session.commit()
        flash('Pet added!')
        return redirect(url_for('add_pet'))

    return render_template('add_pet.html', form=form)

@app.route('/add_service', methods = ['GET', 'POST'])
@login_required
def add_service():

    available_pets = db.session.query(Pet).filter(Pet.user_id == current_user.id)

    pet_list = [(i.id, i.name) for i in available_pets]
    form = AddServiceForm()
    form.pet_name.choices = pet_list

    if form.validate_on_submit():
        service = Service(type_service=form.service_type.data,
                           date=form.date.data,
                           time=form.time.data,
                           notes=form.notes.data,
                           pet_id=form.pet_name.data,
                           pet_name= Pet.query.get(form.pet_name.data).name,
                           user_id=current_user.id)


        db.session.add(service)
        db.session.commit()

        
        flash('Booking Confirmed!')
        return redirect(url_for('welcome_user'))

    return render_template('add_service.html', form=form)



if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True)  