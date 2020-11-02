from flask import redirect, request, render_template, url_for
from flask_wtf.csrf import CSRFProtect
from mast.forms import LoginForm, RegisterForm
from mast import app
import logging

# TODO: change to some valid secret key (this is required by wtf_forms csrf protection)
app.secret_key = b'TODO_CHANGE'
csrf = CSRFProtect(app)

logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('login.html', form=form)
    else:
        form = LoginForm(request.form)
        valid = form.validate()
        print(form.password.errors)
        if valid:
            # TODO: redirect the user to main page
            return 'MAST homepage'
        else:
            return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        form = RegisterForm()
        return render_template('register.html', form=form)
    else:
        form = RegisterForm(request.form)
        valid = form.validate()
        if valid:
            # TODO: add user to database
            return redirect(url_for('login'))
        else:
            return render_template('register.html', form=form)


@app.route('/personal_dashboard')
@app.route('/home')
def home():
    return render_template("personal_dashboard.html", title='Home')


@app.route('/global_dashboard')
def global_dashboard():
    return render_template("global_dashboard.html", title='Global Dashboard')

@app.route('/user_settings')
def user_settings():
    return render_template("user_settings.html", title='User Settings')

@app.route('/integrations')
def integrations():
    return render_template("integrations.html", title='Integrations')
  