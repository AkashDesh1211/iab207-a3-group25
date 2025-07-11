# Import required Flaskform tools and validators.
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateTimeField, RadioField, IntegerField, DecimalField, DateField, TimeField, DateTimeLocalField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed


# Allowed file types for event images
ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

# Form for all login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # Form for all registration information
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

# Form for all event information
class EventsForm(FlaskForm):
    event_name=StringField(validators=[InputRequired('Please enter an event name')])
    start_time=DateTimeLocalField(validators=[InputRequired()])
    end_time=DateTimeLocalField(validators=[InputRequired()])
    STEM_category=RadioField('STEM Category', choices=[('Science', 'Science'),('Information Technology', 'Information Technology'),('Maths', 'Maths'),('Engineering', 'Engineering')])
    event_type=RadioField(choices=[('Online','Online'),('In-Person','In-Person')])
    event_address=StringField(validators=[InputRequired()])
    event_venue=StringField(validators=[InputRequired()])
    ticket_price=DecimalField(validators=[InputRequired()])
    ticket_policy=StringField(validators=[InputRequired()])
    max_num_tickets=StringField(validators=[InputRequired()])
    description=StringField(validators=[InputRequired()])
    image = FileField('Event Image', validators=[
        FileRequired(message = 'Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
    submit = SubmitField()








    # Form for all comment information
class CommentsForm(FlaskForm):
    text = TextAreaField('Comment', [InputRequired()])
    submit = SubmitField('Create Comment')
    


# Form for all order-related information
class OrdersForm(FlaskForm):
    ticket_quantity=StringField("Ticket Quanity", validators=[InputRequired()])
    submit=SubmitField("Book Ticket")

  
