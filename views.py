from flask import Flask, render_template, url_for, request, redirect, jsonify
from datetime import datetime
import numpy as np
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from app import app, db, bcrypt
from db_schema import *
import psutil


def square(n: int):
    return n * n


def is_even():
    number = int(request.args.get('number'))
    if number % 2 == 0:
        return jsonify(message=str(number)+' is even.')
    else:
        return jsonify(message=str(number) + ' is odd.')


def white_noise(amp, time):
    sampling = 10
    t = np.linspace(0, time, time * sampling)
    n = np.random.rand(len(t))
    y = amp * n
    # y = a*m.sin(2*m.pi*f*t) + amp * n
    audio_data = np.int16(y * 2 ** 15)
    values = {}
    for i in range(len(t)):
        values[t[i]] = y[i]
    return values


@app.route('/users', methods=['GET'])
def users():
    users_list = User.query.all()
    return jsonify(users=users_schema.dump(users_list))


@app.route('/performance', methods=['GET'])
def performance():
    performance_list = Performance.query.all()
    return jsonify(performances=performances_schema.dump(performance_list))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        test = User.query.filter_by(username=username).first()
        if test:
            return jsonify(message='That username is taken!'), 409
        else:
            pin = request.form['pin']
            pw_hash = bcrypt.generate_password_hash(pin)
            user = User(username=username, pw_hash=pw_hash)
            db.session.add(user)
            db.session.commit()
            return jsonify(message='User created successfully.'), 201
    elif request.method == 'GET':
        return render_template('register.html')


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        username = request.json['username']
        pin = request.json['pin']
    else:
        username = request.form['username']
        pin = request.form['pin']
    test = User.query.filter_by(username=username).first()
    if test:
        test_user = User.query.filter_by(username=username).first()
        if bcrypt.check_password_hash(test_user.pw_hash, pin):
            access_token = create_access_token(identity=username)
            return jsonify(message='Login succeeded', access_token=access_token), 201
        else:
            return jsonify(message='Wrong password'), 401
    else:
        return jsonify(message='There is no account with that username'), 401


@app.route("/", methods=['POST', 'GET'])
def base():
    return render_template('base.html')


@app.route("/time/", methods=['GET'])
@jwt_required()
def get_time():
    return jsonify(message=str(datetime.now()))


@app.route('/values')
def values():
    if request.args.get('amp').isdigit() and request.args.get('time').isdigit():
        amp = float(request.args.get('amp'))
        time = int(request.args.get('time'))
        return jsonify(white_noise(amp, time))
    else:
        return jsonify(message='Arguments must be numbers.'), 422


@app.route('/square/<int:n>/')
def square(n):
    return jsonify(result=square(n))


@app.route('/random_values')
def random_values():
    return jsonify(white_noise(1, 5))


@app.route('/iseven')
def is_even():
    return is_even()


@app.route('/params', methods=['GET'])
def params():
    return jsonify(cpu_usage=psutil.cpu_percent(), cpu_stats=psutil.cpu_stats(), cpu_freq=psutil.cpu_freq(),
                   logged_users=psutil.users(), disk_usage=psutil.disk_usage('/'),
                   virtual_memory=psutil.virtual_memory())


@app.route('/params/<int:id>/', methods=['GET'])
def params_id(id):
    parameters = Performance.query.filter_by(id=id).first()
    if parameters:
        return jsonify(performance=performance_schema.dump(parameters))
    else:
        return jsonify(message='There is no parameters with that id'), 404


@app.route('/add_params/', methods=['POST'])
def add_params():
    test = Performance.query.filter_by(id=request.form['date']).first()
    if test:
        return jsonify(message='There is already parameters in db from that date.'), 409
    else:
        parameters = Performance(date=request.form['date'], memory_usage=float(request.form['memory_usage']),
                                 CPU_usage=float(request.form['CPU_usage']),
                                 disk_usage=float(request.form['disk_usage']))
        db.session.add(parameters)
        db.session.commit()
        return jsonify(message='You added new parameters!'), 201


@app.route('/update_params/', methods=['PUT'])
def update_params():
    parameters = Performance.query.filter_by(date=request.form['date']).first()
    if parameters:
        parameters.date = request.form['date']
        parameters.memory_usage = float(request.form['memory_usage'])
        parameters.CPU_usage = float(request.form['CPU_usage'])
        parameters.disk_usage = float(request.form['disk_usage'])
        db.session.commit()
        return jsonify(message='You updated parameters!'), 202
    else:
        return jsonify(message='There is no parameters with that id'), 404


@app.route('/delete_params/<int:id>/', methods=['DELETE'])
def delete_params(id):
    parameters = Performance.query.filter_by(id=id).first()
    if parameters:
        db.session.delete(parameters)
        db.session.commit()
        return jsonify(message='You deleted parameters from ' + parameters.date + ' !'), 202
    else:
        return jsonify(message='There is no parameters with that id'), 404


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


@app.cli.command('db_seed')
def db_seed():
    user1 = User(username='first', pw_hash=bcrypt.generate_password_hash('1234'))
    user2 = User(username='second', pw_hash=bcrypt.generate_password_hash('abcd'))
    user3 = User(username='third', pw_hash=bcrypt.generate_password_hash('1234'))
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    parameters = Performance(date=str(datetime.now()), memory_usage=psutil.virtual_memory()[2],
                             CPU_usage=psutil.cpu_percent(), disk_usage=psutil.disk_usage('/')[3])
    db.session.add(parameters)
    db.session.commit()
    print('Database seeded!')
