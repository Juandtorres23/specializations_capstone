from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateField, TimeField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from myproject.model import User


class AddPetForm(FlaskForm):
    name = StringField('Pet Name:', validators = [DataRequired()])
    pet_type = SelectField('Pet Type:',
                            choices=[('Dog', 'Dog'), ('Cat', 'Cat')], 
                            validators=[DataRequired()]) 
    size = SelectField('Pet Size:',
                        choices=[('Small', 'Small'), ('Medium', 'Medium'),
                        ('Large', 'Large')], validators=[DataRequired()]) 
    weight = StringField('Weight:', validators = [DataRequired()])
    pet_description = TextAreaField('Description:')
    pet_img = FileField("Pet Pic:")
    submit = SubmitField('Add Pet')

def get_pet_form(type_pet, pet_size, desc):
    class Editpet(AddPetForm):
        pet_type = SelectField('Pet Type:', choices=[('Dog', 'Dog'), 
                                ('Cat', 'Cat')], validators=[DataRequired()],
                                default=type_pet) 
        size = SelectField('Pet Size:',
                            choices=[('Small', 'Small'), ('Medium', 'Medium'),
                            ('Large', 'Large')], validators=[DataRequired()],
                            default=pet_size) 
        pet_description = TextAreaField('Description:', default=desc) 
    return Editpet()


class AddServiceForm(FlaskForm):
    service_type = SelectField('Service:', choices=[('Boarding', 'Boarding'), 
                                ('House Sitting', 'House Sitting'), 
                                ('Dog Walking', 'Dog Walking')],
                                validators= [DataRequired()])
    date = DateField('Date:', validators= [DataRequired()])
    time = TimeField('Time:', validators= [DataRequired()])
    # maybe add a durations field
    pet_name = SelectField('Pet Name', coerce=int, validators= [DataRequired()])
    notes =  TextAreaField('Pet Notes:', validators= [DataRequired()])
    submit = SubmitField('Add Appoitment')

def get_service_form(services, name, clock, note):
    class Editservice(AddServiceForm):
        time = TimeField('Time:', validators= [DataRequired()], default=clock)
        notes = TextAreaField('Pet Notes:', validators= [DataRequired()], default=note)
        service_type = SelectField('Service:', choices=[('Boarding', 'Boarding'), 
                                ('House Sitting', 'House Sitting'), 
                                ('Dog Walking', 'Dog Walking')],
                                validators= [DataRequired()], default=services)
        pet_name = SelectField('Pet Name', coerce=int, validators= [DataRequired()], default=name)
    return Editservice()


class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Log In')

# remember_me= BooleanField('Remember me')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    username = StringField('Username', validators = [DataRequired()])
    phone = StringField('Phone', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired(), EqualTo('pass_confirm', message = 'Password must match!')])
    pass_confirm = PasswordField('Confirm Password', validators = [DataRequired()])
    submit = SubmitField('Register!')

    def check_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Your email has been already registered!')

    def check_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Username is taken!')