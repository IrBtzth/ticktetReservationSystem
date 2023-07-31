import datetime
from .. import db
from webapp.auth.models import User 


class Bookings(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    code = db.Column(db.String(), nullable=False)
    class_ctg = db.Column(db.String(), nullable=False)
    date = db.Column(db.Date(), default=datetime.datetime.utcnow)
    seat = db.Column(db.Integer(), nullable=False)

    schedules_id = db.Column(db.Integer, db.ForeignKey('schedules.id'))
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Schedules(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    fcFee = db.Column(db.Float(), nullable=False)
    scFee = db.Column(db.Float(), nullable=False)
    date = db.Column(db.Date(), default=datetime.datetime.utcnow)
    times = db.Column(db.Time())

    bookings = db.relationship('Bookings', backref='schedules',lazy='dynamic')

    routes_id = db.Column(db.Integer, db.ForeignKey('routes.id'))
    trains_id = db.Column(db.Integer, db.ForeignKey('trains.id'))

class Routes(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    fromRoute = db.Column(db.String(100), nullable=False)
    toRoute = db.Column(db.String(100), nullable=False)

    schedules = db.relationship('Schedules', backref='routes',lazy='dynamic')
    def __repr__(self):
        return "{a} to {b}".format(a=self.fromRoute,b=self.toRoute)

class Trains(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    trainName = db.Column(db.String(80), nullable=False)
    fcSeat = db.Column(db.Integer(), nullable=False)
    scSeat = db.Column(db.Integer(), nullable=False)

    schedules = db.relationship('Schedules', backref='trains',lazy='dynamic')
    def __repr__(self):
        return "{}".format(self.trainName)
    
    
class Payment(db.Model):

    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    amount = db.Column(db.String(255), nullable=False)
    ref = db.Column(db.String(255), nullable=False)

    bookings = db.relationship('Bookings', backref='payment',lazy='dynamic')

    


class Feedback(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    message = db.Column(db.Text(400), nullable=False)
    response = db.Column(db.Text(400), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
