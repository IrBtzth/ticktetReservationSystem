from flask_wtf import FlaskForm as Form
from flask_wtf import RecaptchaField
from wtforms import StringField, PasswordField, BooleanField,EmailField,IntegerField,SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, URL, ValidationError
from .models import User
from . import authenticate
import phonenumbers


class LoginForm(Form):
    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField("Remember Me")

    submit = SubmitField('Login')

    def validate(self,extra_validators=None):
        check_validate = super(LoginForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        if not authenticate(self.username.data, self.password.data):
            self.username.errors.append('Invalid username or password')
            return False
        return True


class OpenIDForm(Form):
    openid = StringField('OpenID URL', [DataRequired(), URL()])


class UserForm(Form):
    username = StringField('Username', [DataRequired(), Length(max=255)])
    name = StringField('Name', [DataRequired(), Length(max=255)])
    lastName=StringField('Last name', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired(), Length(min=8)])
    confirm = PasswordField('Confirm Password', [
        DataRequired(),
        EqualTo('password')
    ])
    email = EmailField('Email address', validators=[DataRequired()]) 
    phone = StringField('Phone', validators=[DataRequired()])

    recaptcha = RecaptchaField()
    submit = SubmitField()
    def validate_phone(form, field):
        if len(field.data) > 16:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+1"+field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')

    def validate(self,extra_validators=None):
        check_validate = super(UserForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        user = User.query.filter_by(username=self.username.data).first()

        # Is the username already being used
        if user:
            self.username.errors.append("User with that name already exists")
            return False

        return True