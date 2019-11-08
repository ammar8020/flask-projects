from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from project1.models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = StringField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = StringField(
        "Password", validators=[DataRequired(), Length(min=4, max=20)]
    )
    confirm_password = StringField(
        "Confirm Password",
        validators=[DataRequired(), Length(min=4, max=20), EqualTo("password")],
    )
    first_name = StringField(
        "First Name", validators=[DataRequired(), Length(min=2, max=40)]
    )
    last_name = StringField(
        "Last Name", validators=[DataRequired(), Length(min=2, max=40)]
    )
    submit = SubmitField("Register Now")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError("Email is not available. Please try a different one.")
