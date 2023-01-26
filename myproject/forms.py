from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError

from model import User, Pet, Service

class AddPetForm(FlaskForm):
    pet_name = StringField('Pet Name', validators = [DataRequired()])
    pet_type = StringField('Pet Type', validators = [DataRequired()])
    size = StringField('Pet Size', validators = [DataRequired()])
    weight = StringField('Weight', validators = [DataRequired()])
    submit = SubmitField('Add Pet')

class AddServiceForm(FlaskForm):
    service_type = StringField('Service', validators= [DataRequired()])
    date = StringField('Date', validators= [DataRequired()])
    time = StringField('Time', validators= [DataRequired()])
    pet_id =  StringField('Pet Id', validators= [DataRequired()])
    notes =  StringField('Pet Notes', validators= [DataRequired()])
    submit = SubmitField('Add Appoitment')


class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    Username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired(), EqualTo('pass_confirm', message = 'Password must match!')])
    pass_confirm = PasswordField('Confirm Password', validators = [DataRequired()])
    submit = SubmitField('Register!')

    def check_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Your email has been already registered!')

    def check_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Username is taken!')