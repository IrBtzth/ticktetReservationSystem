from flask_wtf import FlaskForm
from wtforms_alchemy import ModelForm
from wtforms import TimeField, DateField,StringField,EmailField, SelectField, SubmitField,IntegerField, PasswordField, BooleanField, ValidationError,TextAreaField, FormField,FieldList
from wtforms.validators import DataRequired, EqualTo, Length,Regexp
from wtforms_alchemy import ModelForm
from datetime import datetime
#from .models import Schedules
from .models import Schedules
from wtforms_sqlalchemy.fields import QuerySelectField

class FeedbackForm(FlaskForm):
    message = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('Submit')




class newBookingForm(FlaskForm):
    
    numberTickets = IntegerField(label= 'Number of tickets (if you are the only one, leave as it is):',default=1, validators=[DataRequired()])
    className = SelectField(label= 'Class:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SchedulesForm(FlaskForm):
    fcFee = StringField(label= 'First class fee:', validators=[DataRequired()])
    scFee = StringField(label= 'Second class fee:', validators=[DataRequired()])
    date = DateField('Date:', format='%Y-%m-%d', validators=[DataRequired()])
    times = TimeField('Time:', format='%H:%M', validators=[DataRequired()])
    routes_id = SelectField(label= 'Routes:', validators=[DataRequired()])
    trains_id = SelectField(label= 'Trains:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RoutesForm(FlaskForm):
    fromRoute = StringField(label= 'From:', validators=[DataRequired()])
    toRoute = StringField(label= 'To:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TrainsForm(FlaskForm):
    trainName = StringField(label= 'Train name:', validators=[DataRequired()])
    fcSeat = IntegerField(label= 'First class seat:', validators=[DataRequired()])
    scSeat = IntegerField(label= 'Second class seat:', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ScheForm(ModelForm):
    class Meta:
        model = Schedules

    booking = QuerySelectField(
        query_factory=lambda: Schedules.query.all(),
        get_pk=lambda a: a.id,
        get_label=lambda a: a.fcFee,
        allow_blank=False,
    )