from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField, BooleanField,SubmitField
from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError
#from application.models import User


class LoginForm(FlaskForm):
    email = EmailField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=8,max=15)])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired(),Length(min=2,max=50)])
    email = EmailField("Email",validators=[DataRequired(),Email()])
    password= PasswordField("Password",validators=[DataRequired(),Length(min=8,max=15)])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(),Length(min=6,max=15), EqualTo('password')])
    submit = SubmitField("Signup")

    #def validate_email(self,email):
    #    user = User.objects(email=email.data).first()
    #    if user:
    #        raise ValidationError("Email is already in use. Pick another one.")