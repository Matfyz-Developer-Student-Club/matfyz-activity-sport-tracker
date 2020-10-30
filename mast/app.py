from flask import Flask, redirect, request, render_template, url_for
from flask_wtf.csrf import CSRFProtect
from mast.forms import LoginForm, RegisterForm, log_form_submit

app = Flask(__name__)

# TODO: change to some valid secret key (this is required by wtf_forms csrf protection)
app.secret_key = b'TODO_CHANGE'
csrf = CSRFProtect(app)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('login.html', form=form)
    else:
        form = LoginForm(request.form)
        valid = form.validate()
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


if __name__ == '__main__':
    app.run(debug=True)
