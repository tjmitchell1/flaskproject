# External Packages
from flask import escape, Flask, session, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

# System Packages
import re

# Project Packages
from src import app, db
from src.models import User

@app.route('/')
@app.route('/index')
def index():
    if 'username' in session:
        return render_template('brackets.html', username=escape(session['username']))
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
            new_user = User(username=request.form['username'], password_hash=generate_password_hash(request.form['username']))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            error = 'User already exists.'
            return render_template('signup.html', error=error)

@app.route('/brackets', methods=['GET', 'POST'])
def brackets():
    if request.method == 'POST':
        reg = r'^[\{\}\[\]\(\)]+$'
        if not re.match(reg, request.form['bracket']):
            return render_template('brackets.html', value=None, error='Please enter a valid string.')
        running_list = []
        opposite_char = {
            ')': '(',
            ']': '[',
            '}': '{'
        }
        for char in request.form['bracket']:
            if char in opposite_char:
                if len(running_list) > 0 and running_list[-1] == opposite_char[char]:
                    del running_list[-1]
                else:
                    return render_template('brackets.html', value=False, error=None)
            else:
                running_list.append(char)
        if len(running_list) != 0:
            return render_template('brackets.html', value=False, error=None)
        return render_template('brackets.html', value=True, error=None)
    else:
        if 'username' in session:
            return render_template('brackets.html', username=escape(session['username']))
        else:
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
