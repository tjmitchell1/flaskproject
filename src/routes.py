# External Packages
from flask import escape, Flask, session, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

# System Packages
import re

# Project Packages
from src import app, db
from src.models import User, History

from src.scripts.bracket_balance import bracket_balance

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('brackets'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None or not check_password_hash(user.password_hash, request.form['password']):
            error = 'Invalid Username or Password. Please try again.'
            return render_template('login.html', error=error)
        else:
            session['username'] = request.form['username']
            return redirect(url_for('brackets'))
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        if len(request.form['password']) is 0 or request.form['password'] != request.form['confirmpassword']:
            error = 'Password confirmation must match the password.'
            return render_template('signup.html', error=error)
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None:
            new_user = User(username=request.form['username'], password_hash=generate_password_hash(request.form['password']))
            db.session.add(new_user)
            db.session.commit()
            session['username'] = request.form['username']
            return redirect(url_for('brackets'))
        else:
            error = 'User already exists.'
            return render_template('signup.html', error=error)

@app.route('/brackets', methods=['GET', 'POST'])
def brackets():
    error = None
    value = None
    user = None
    history = []
    if 'username' in session:
        user = User.query.filter_by(username=escape(session['username'])).first()
    if request.method == 'POST':
        reg = r'^[\{\}\[\]\(\)]+$'
        if not re.match(reg, request.form['bracket']):
            error = 'Please enter a valid string.'
        else:
            value = bracket_balance(request.form['bracket'])
            new_history = History(user_id=user.id, bracket_string=request.form['bracket'], bracket_value=value)
            db.session.add(new_history)
            db.session.commit()
    else:
        if user is None:
            return redirect(url_for('login'))
    if user is not None:
        history = History.query.filter_by(user_id=user.id).order_by(History.id.desc()).limit(5).all()
    return render_template('brackets.html', value=value, error=error, history=history, username=escape(session['username']))   

@app.route('/history')
def history():
    user = User.query.filter_by(username=escape(session['username'])).first()
    history = History.query.filter_by(user_id=user.id).order_by(History.id.desc()).all()
    return render_template('history.html', history=history, username=escape(session['username']))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
