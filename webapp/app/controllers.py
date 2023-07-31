from datetime import datetime, date
from sqlalchemy import desc, func
from flask import render_template, Blueprint, flash, redirect, url_for, current_app, abort, request,Response
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import jinja2.exceptions
from .forms import RoutesForm, SchedulesForm, TrainsForm,newBookingForm,FeedbackForm, ScheForm
from webapp.repositories.CrudRepository import CrudRepository, formChoices
from .models import Routes, Schedules, Trains, Bookings, Payment, Feedback
from ..auth.models import User,Role
from ..auth.forms import UserForm
from webapp import db
from fpdf import FPDF
from flask import make_response
import pdfkit
import stripe
from wtforms_sqlalchemy.orm import model_form
import string
import random
from ..auth import has_role


app_blueprint = Blueprint(
    'app',
    __name__,
    template_folder='../templates'
)

stripe.api_key = 'sk_test_51NMD53JljMONOdDhgNaT0hdB11LX5QUFBGDQjaR9fJn7inhGpftnZHNdr751sJgJAVEEUFndcKImtgIrN9ilXIU200OnQ3zz7D'
YOUR_DOMAIN = 'http://127.0.0.1:5000'


@app_blueprint.route('/feedback_user/feedback_userCreate', methods=['GET', 'POST'])
@login_required
@has_role('Customer')
def feedback_userCreate():
    form = FeedbackForm()
    if form.validate_on_submit():
        
        createRoute = CrudRepository(Feedback, db)
        createRoute.create(message=form.message.data, response='None')
        return redirect(url_for('app.feedback_user')) 

    flash('There was an error adding your message')
    return redirect(url_for('app.feedback_user'))
    
@app_blueprint.route('/feedback_user')
@login_required
@has_role('Customer')
def feedback_user():
    form = FeedbackForm()
    feedbacks=Feedback.query.all()
    return render_template('feedback_user.html', form=form, feedbacks=feedbacks)

#---- FEEDBACK USER----

@app_blueprint.route('/feedback/feedbackUpdate/<int:id>', methods=['GET', 'POST'])
@login_required
@has_role('Customer')
def feedbackUpdate(id):
    form = FeedbackForm()
    if form.validate_on_submit():
        
        createRoute = CrudRepository(Feedback, db)
        createRoute.update(id=id,response=form.message.data)
        return redirect(url_for('app.feedback')) 

    flash('There was an error adding your message')
    return redirect(url_for('app.feedback'))
    
@app_blueprint.route('/feedback')
@login_required
@has_role('Customer')
def feedback():
    form = FeedbackForm()
    feedbacks=Feedback.query.all()
    return render_template('feedback.html', form=form, feedbacks=feedbacks)

#---- FEEDBACK ----

@app_blueprint.route('/homepage/')
def homepage():
    r=request.url_rule.endpoint
    return render_template('homepage.html',r=r)

#---- HOMEPAGE ----

@app_blueprint.route('/success/<string:var>/<int:id>', methods=['POST', 'GET'])
@login_required
@has_role('Customer')
def success(var,id):

    if 'First class' in var:
        className='First class'
    elif 'Second class' in var:
        className='Second class'
    
    ref=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(7))
    amount= float(var.replace('First class','').replace('Second class','').replace("''",'').replace('[','').replace(']','').replace(',','').replace(' ',''))

    createRoute = CrudRepository(Payment, db)
    createRoute.create(amount=amount, ref=ref)
    payment_id=max([value.id for value in Payment.query.all()])
        
    seat=''.join(random.choices(string.ascii_uppercase, k=1)) + ''.join(random.choices(string.digits, k=3))
    code=''.join(random.choices( string.digits, k=7))

    createRoute = CrudRepository(Bookings, db)
    createRoute.create(code=code, class_ctg=className, date=date.today(),seat=seat,schedules_id=id, payment_id=payment_id,user_id=current_user.id)

    payments= Payment.query.all()
    bookings= Bookings.query.all()
    return render_template('success.html',var=var,payments=payments,bookings=bookings)


@app_blueprint.route('/create-checkout-session/<string:var>/<int:id>', methods=['POST', 'GET'])
@login_required
@has_role('Customer')
def create_checkout_session(var,id):

    try:

        checkout_session = stripe.checkout.Session.create(
            line_items=[{ 
                'price':'price_1NT5TuJljMONOdDh7kVWpvQp',
                'quantity':1
            }],
            mode='payment',
            success_url=YOUR_DOMAIN + url_for('app.success', var=var, id=id),
            cancel_url=YOUR_DOMAIN + '/cancel.html',
            )
        
        
    except Exception as e:

        return str(e)
    return redirect(checkout_session.url, code=303)
    

#---- PAYMENT ----



@app_blueprint.route('/bookingCreate/<int:id>', methods=['GET', 'POST'])
@login_required
@has_role('Customer')
def bookingCreate(id):
    
    schedule=Schedules.query.get_or_404(id)
    request.form.get('seats', type = int)
    
 
    numberTickets = request.form.get('seats', type = int)
    className=None

    amount=0
    if request.form.get('classFee') == '0':
        className = ['First class',int(schedule.fcFee)]
        amount=schedule.fcFee*numberTickets
    else:
        className= ['Second class',int(schedule.scFee)]
        amount=schedule.scFee*numberTickets
    
    booking_items=[className[0],amount]
    return render_template('home.html', datetime=datetime,booking_items=booking_items, schedule_id=schedule.id, numberTickets=numberTickets, className=className,amount=amount, scheduleRoute=schedule.routes)



@app_blueprint.route('/newBooking', methods=['GET', 'POST'])
@login_required
@has_role('Customer')
def newBooking():
    schedules= Schedules.query.all()
    
    return render_template('newBooking.html', schedules=schedules, datetime=datetime)
    
    

#---- USER ---- 

@app_blueprint.route('/reportDonwload/<int:id>')
def reportDonwload(id):
    
    
    schedule= Schedules.query.get_or_404(id)
    bookings= Bookings.query.filter_by(schedules_id=schedule.id)
    html = render_template(
        "pdfReport.html",
        schedule=schedule, bookings=bookings, datetime=datetime)
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response


@app_blueprint.route('/report')
def report():
    
    schedules=Schedules.query.all()
    return render_template('report.html', schedules=schedules)

#---- REPORT ----

@app_blueprint.route('/trains/trainDelete/<int:id>', methods=['GET', 'POST'])
def trainDelete(id):
   
    createRoute = CrudRepository(Trains, db)
    createRoute.delete(id=id)
    return redirect(url_for('app.trains')) 

    


@app_blueprint.route('/trains/trainUpdate/<int:id>', methods=['GET', 'POST'])
def trainUpdate(id):

    form = TrainsForm()
    if form.validate_on_submit():
        
        createRoute = CrudRepository(Trains, db)
        createRoute.update(id=id,fcSeat=form.fcSeat.data, scSeat=form.scSeat.data)
        return redirect(url_for('app.trains')) 

    flash('There was an error editing your train')
    return redirect(url_for('app.trains'))
  

@app_blueprint.route('/trains/trainCreate', methods=['GET', 'POST'])
def trainCreate():
    form = TrainsForm()
    if form.validate_on_submit():
        
        createRoute = CrudRepository(Trains, db)
        createRoute.create(trainName=form.trainName.data, fcSeat=form.fcSeat.data, scSeat=form.scSeat.data)
        return redirect(url_for('app.trains')) 

    flash('There was an error adding your train')
    return redirect(url_for('app.trains'))
    

@app_blueprint.route('/trains')
def trains():
    form = TrainsForm()
    trains=Trains.query.all()
    return render_template('trains.html', form=form, trains=trains)

#---- TRAINS ----

@app_blueprint.route('/schedules/scheduleDelete/<int:id>', methods=['GET', 'POST'])
def scheduleDelete(id):
   
    createSchedule= CrudRepository(Schedules, db)
    createSchedule.delete(id=id)
    return redirect(url_for('app.schedules')) 

    


@app_blueprint.route('/schedules/scheduleUpdate/<int:id>', methods=['GET', 'POST'])
def scheduleUpdate(id):

    form = SchedulesForm()
    form.trains_id.choices= formChoices(Trains)
    form.routes_id.choices= formChoices(Routes)

    if form.validate_on_submit():
        
        createRoute = CrudRepository(Schedules, db)
        createRoute.update(id=id,fcFee=form.fcFee.data, scFee=form.scFee.data,date=form.date.data,times=form.times.data,routes_id=form.routes_id.data,trains_id=form.trains_id.data)
        return redirect(url_for('app.schedules')) 

    flash('There was an error editing your schedule')
    return redirect(url_for('app.schedules'))
  

@app_blueprint.route('/schedules/scheduleCreate', methods=['GET', 'POST'])
def scheduleCreate():

    form = SchedulesForm()

    form.trains_id.choices= formChoices(Trains)
    form.routes_id.choices= formChoices(Routes)

    train=Trains.query.get(form.trains_id.data)
    route=Routes.query.get(form.routes_id.data)


    if form.validate_on_submit():
        
        createSchedule = CrudRepository(Schedules, db)
        schedule=createSchedule.create(fcFee=form.fcFee.data, scFee=form.scFee.data,date=form.date.data,times=form.times.data, routes_id=route.id, trains_id=train.id)
        db.session.commit()

        return redirect(url_for('app.schedules')) 

    flash('There was an error adding your schedule')
    return redirect(url_for('app.schedules'))
    

@app_blueprint.route('/schedules')
def schedules():
    form = SchedulesForm()
    
    form.trains_id.choices= formChoices(Trains)
    form.routes_id.choices= formChoices(Routes)
   
    schedules=Schedules.query.all()
    routes=Routes.query.all()
    trains=Trains.query.all()
    return render_template('schedules.html', form=form, schedules=schedules)

#---- SCHEDULES ----

@app_blueprint.route('/routes/routeDelete/<int:id>', methods=['GET', 'POST'])
def routeDelete(id):
   
    createRoute = CrudRepository(Routes, db)
    createRoute.delete(id=id)
    return redirect(url_for('app.routes')) 



@app_blueprint.route('/routes/routeUpdate/<int:id>', methods=['GET', 'POST'])
def routeUpdate(id):

    form = RoutesForm()
    if form.validate_on_submit():
        
        createRoute = CrudRepository(Routes, db)
        createRoute.update(id=id,fromRoute=form.fromRoute.data, toRoute=form.toRoute.data)
        return redirect(url_for('app.routes')) 

    flash('There was an error editing your route')
    return redirect(url_for('app.routes'))
  

@app_blueprint.route('/routes/routeCreate', methods=['GET', 'POST'])
def routeCreate():
    form = RoutesForm()
    if form.validate_on_submit():
        
        createRoute = CrudRepository(Routes, db)
        createRoute.create(fromRoute=form.fromRoute.data, toRoute=form.toRoute.data)
        return redirect(url_for('app.routes')) 

    flash('There was an error adding your route')
    return redirect(url_for('app.routes'))
    

@app_blueprint.route('/routes')
def routes():
    form = RoutesForm()
    routes=Routes.query.all()
    return render_template('routes.html', form=form, routes=routes)

@app_blueprint.route('/index')
def index():

    return render_template('login.html')

#---- USERS ----

@app_blueprint.route('/userDelete/<int:id>', methods=['GET', 'POST'])
def userDelete(id):
    
    createRoute = CrudRepository(User, db)
    createRoute.delete(id=id)
    return redirect(url_for('app.users'))

@app_blueprint.route('/users')
def users():

    form= UserForm()
    users= User.query.all()
    return render_template('users.html', users=users,form=form)
