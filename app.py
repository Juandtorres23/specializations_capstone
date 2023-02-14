import os
import uuid as uuid
from myproject import app, db, connect_to_db, ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from flask import render_template, redirect, request, url_for, flash, abort, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from datetime import timedelta 
from flask_uploads import configure_uploads, IMAGES, UploadSet 
from werkzeug.utils import secure_filename

from myproject.model import User, Pet, Service
from myproject.forms import LoginForm, RegistrationForm, AddPetForm, AddServiceForm, get_service_form, get_pet_form

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/welcome')
@login_required
def welcome_user():
    pets = current_user.get_pets()
    services = current_user.get_services()
    return render_template('profile.html', pets=pets, services=services, name=current_user.username)

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
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('welcome_user')
            flash('Logged in Successfully!')
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
        if request.files['pet_img']:
            pet_pic = request.files['pet_img']
            pic_filename = secure_filename(pet_pic.filename)
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            saver = request.files['pet_img']

            pet = Pet(name=form.name.data,
                        pet_type=form.pet_type.data,
                        size=form.size.data,
                        weight=form.weight.data,
                        pet_description=form.pet_description.data,
                        user_id=current_user.id,
                        pet_pic=pic_name)

            db.session.add(pet)
            db.session.commit()
            saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
            flash('Pet added!')
            return redirect(url_for('add_pet'))
        else:
            pet = Pet(name=form.name.data,
                        pet_type=form.pet_type.data,
                        size=form.size.data,
                        weight=form.weight.data,
                        pet_description=form.pet_description.data,
                        user_id=current_user.id,
                        pet_pic=None)
            db.session.add(pet)
            db.session.commit()
            flash('Pet added!')
            return redirect(url_for('add_pet'))
    return render_template('add_pet.html', form=form)


@app.route('/update_pet/<pet_id>', methods = ['GET', 'POST'])
def update_pet(pet_id):
    pets = current_user.get_pets()
    pet = Pet.query.filter_by(id=pet_id).first()
    form = get_pet_form(pet.pet_type, pet.size, pet.pet_description)

    if request.method == 'POST':
        if form.validate_on_submit():
            pet.name = form.name.data,
            pet.pet_type = form.pet_type.data,
            pet.size = form.size.data,
            pet.weight=form.weight.data,
            pet.pet_description=form.pet_description.data,
            if request.files['pet_img']:
                pet.pet_pic=request.files['pet_img']
                pic_filename = secure_filename(pet.pet_pic.filename)
                pic_name = str(uuid.uuid1()) + "_" + pic_filename
                pet.pet_pic = pic_name
                saver = request.files['pet_img']
                
                db.session.commit()
                saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                flash("Updated pet successfully!")
                return redirect(url_for('update_pet', pet_id=pet.id))
            else:
                db.session.commit()
                flash("Updated pet successfully!")
                return redirect(url_for('update_pet', pet_id=pet.id))
        else:
            return redirect(url_for('welcome_user'))
    else:
        return render_template("update_pet.html", pets=pets, pet=pet, form=form, pet_id=pet_id)

@app.route('/delete_pet/<int:pet_id>')
def delete_pet(pet_id):
    pet_to_delete = Pet.query.filter_by(id=pet_id).first()
    try:
        db.session.delete(pet_to_delete)
        db.session.commit()
        flash("Pet Deleted Successfully!")
        return redirect(url_for('welcome_user'))
    except:
        flash("Whoops! There was a problem. Try again!")
        return render_template('profile.html', pet_id=pet_id)

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

@app.route('/update_service/<service_id>', methods = ['GET', 'POST'])
def update_service(service_id):
    service = Service.query.filter_by(id=service_id).first()
    available_pets = db.session.query(Pet).filter(Pet.user_id == current_user.id)
    pet_list = [(i.id, i.name) for i in available_pets]
    form = get_service_form(service.time, service.type_service, service.pet_name, service.notes)
    form.pet_name.choices = [(service.pet_id, service.pet_name)] + pet_list

    if request.method == 'POST':
        if form.validate_on_submit():
            service.type_service = form.service_type.data,
            service.date = form.date.data,
            service.time = form.time.data,
            service.pet_id = form.pet_name.data,
            service.pet_name = Pet.query.get(form.pet_name.data).name,
            service.notes = form.notes.data
        
            db.session.commit()
            flash("Appointment Updated Successfully!")
            return redirect(url_for('welcome_user'))
        else:
            flash("Something went wrong!")
            return redirect(url_for('update_service', form=form, service_id=service.id))
    else:
        return render_template("update_service.html", service=service, form=form, service_id=service_id, pet_name=service.pet_name, time=service.time)

@app.route('/delete_app/<int:service_id>')
def delete_service(service_id):
    service_to_delete = Service.query.filter_by(id=service_id).first()
    try:
        db.session.delete(service_to_delete)
        db.session.commit()
        flash("Appointment Deleted Successfully!")
        return redirect(url_for('welcome_user'))
    except:
        flash("Whoops! There was a problem deleting appointment. Try again!")
        return render_template('profile.html', service_id=service_id)

if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True)  