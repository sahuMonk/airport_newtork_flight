from main import app
from models import db, UserModel, FlightModel
from flask import redirect, render_template, flash, url_for, request
from flask_login import login_required, current_user, logout_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash
import string
import validators
import secrets


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/flight_details")
@login_required
def flight_details():
    if current_user.role != 'admin':
        logout_user()
        flash('You do not have required authorization')
        return redirect(url_for('auth.login'))
    else:
        return render_template("flight_details.html")


@app.route("/flight_details", methods=["POST"])
def flight_details_post():
    source = request.form.get('source')
    destination = request.form.get('destination')
    airline = request.form.get('airline')
    departure = request.form.get('departure')
    arrival = request.form.get('arrival')
    halt_time = request.form.get('halt_time')

    flight = FlightModel(source=source, destination=destination, airline=airline, departure=departure,
                         arrival=arrival, halt_time=halt_time)
    db.session.add(flight)
    db.session.commit()
    flash('Details Submitted', 'success')
    return redirect(url_for('flight_details'))


@app.route('/register_supervisor')
@login_required
def register():
    if current_user.role != 'admin':
        logout_user()
        flash('You do not have required authorization')
        return redirect(url_for('auth.login'))
    else:
        return render_template("register_supervisor.html")


mail = Mail(app)


@app.route('/register_supervisor', methods=['POST'])
def register_post():
    name = request.form.get('name')
    airport = request.form.get('airport')
    number = request.form.get('number')
    email = request.form.get('email')

    user = UserModel.query.filter_by(email=email).first()

    error = False
    if user:
        flash('Email address already exists.', 'error')
        error = True

    if not validators.email(email):
        flash('Enter a valid email', 'error')
        error = True

    if not set(name).issubset(string.ascii_letters + " "):
        flash('Name can only contain alphabets.', 'error')
        error = True

    if error:
        return redirect(url_for('auth.register'))

    else:
        letters = string.ascii_letters
        digits = string.digits
        special_chars = string.punctuation

        alphabet = letters + digits + special_chars

        pwd_len = 8

        pwd = ''
        for i in range(pwd_len):
            pwd += ''.join(secrets.choice(alphabet))

        new_user = UserModel(name=name, airport=airport, number=number, email=email,
                             password=generate_password_hash(pwd, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        msg = Message('login password', sender="", recipients=email)
        msg.body = pwd
        mail.send(msg)
        flash('User successfully registered.', 'success')


@app.route("/view_flights")
def view_flights():
    option = FlightModel.query.all()

    return render_template("flights.html", option=option)


@app.route("/arrival")
def arrival():
    return render_template("arrival.html")


@app.route("/arrival", methods=["POST"])
def arrival_post():
    airport = request.form.get('airport')
    terminal = request.form.get('terminal')

    source = FlightModel.query.filter_by(destination=airport, airline=terminal).all()
    return render_template("arrival.html", source=source)


@app.route("/departure")
def departure():
    return render_template("departure.html")


@app.route("/departure", methods=["POST"])
def departure_post():
    airport = request.form.get('airport')
    terminal = request.form.get('terminal')

    curr = FlightModel.query.filter_by(departure=airport, airline=terminal).all()
    return render_template("arrival.html", curr=curr)


@app.route("/flight_delay_detail")
@login_required
def flight_delay_detail():
    port = current_user.airport

    curr = FlightModel.query.filter_by(source=port).all()
    return render_template("flight_delay_detail", curr=curr)


@app.route("/delay_time/<int:flight_number>", methods=['GET', 'POST'])
def delay_time(flight_number):
    delay_update = FlightModel.query.get(flight_number)
    if request.method == 'POST':
        delay_update.delay_time = request.form['delay_time']
        try:
            db.session.commit()
            delay_update.departure = delay_update.departure + delay_update.delay_time
            delay_update.arrival = delay_update.arrival + delay_update.delay_time
            db.session.commit()
            return redirect('/flight_delay_detail')
        except:
            return "error"
    else:
        return render_template('delay_time.html', delay_update=delay_update)


@app.route("/flight_timing")
@login_required
def flight_timing():
    desti = current_user.airport
    flights = FlightModel.query.filter_by(destination=desti).all()
    return render_template("flight_timing.html", flights=flights)
