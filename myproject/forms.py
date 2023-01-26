from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError

from model import User, Pet, Service


class AddPetForm(FlaskForm):
    pet_name = StringField('Pet Name:', validators = [DataRequired()])
    pet_type = SelectField('Pet Type:',
                            choices=[('dog', 'Dog'), ('cat', 'Cat')], 
                            validators=[DataRequired()]) 
    size = SelectField('Pet Size:',
                        choices=[('small', 'Small'), ('medium', 'Medium'),
                        ('large', 'Large')], validators=[DataRequired()]) 
    weight = StringField('Weight:', validators = [DataRequired()])
    submit = SubmitField('Add Pet')


class AddServiceForm(FlaskForm):
    service_type = SelectField('Service:', choices=[('boarding', 'Boarding'), 
                                ('house_sitting', 'House Sitting'), 
                                ('dog_walk', 'Dog Walking')],
                                validators= [DataRequired()])
    date = DateField('Date:', validators= [DataRequired()])
    time = TimeField('Time:', validators= [DataRequired()])
    # maybe add a durations field
    # need to check how to grab the pet id from the current user
    pet_id = StringField('Pet Id', validators= [DataRequired()])
    notes =  TextAreaField('Pet Notes:', validators= [DataRequired()])
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