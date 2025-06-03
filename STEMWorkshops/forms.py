from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateTimeField, RadioField, IntegerField, DecimalField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

# creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    phoneno=StringField("Phone Number", validators=[InputRequired()])
    address=StringField("Home Address", validators=[InputRequired()])
    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")

class EventsForm(FlaskForm):
    event_name=StringField(validators=[InputRequired('Please enter an event name')])
    event_start=DateTimeField(validators=[InputRequired()])
    event_end=DateTimeField(validators=[InputRequired()])
    stem_category=RadioField(choices=[('Science', 'Science'),('Information Technology', 'Information Technology'),('Maths', 'Maths'),('Engineering', 'Engineering')])
    event_type=RadioField(choices=[('Online','Online'),('In-Person','In-Person')])
    event_venue=StringField(validators=[InputRequired()])
    ticket_price=DecimalField(validators=[InputRequired()])
    ticket_policy=StringField(validators=[InputRequired()])
    max_num_tickets=StringField(validators=[InputRequired()])
    description=StringField(validators=[InputRequired()])
    image = FileField('Destination Image', validators=[
        FileRequired(message = 'Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])