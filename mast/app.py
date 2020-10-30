from flask import Flask, redirect, request, render_template, url_for
from mast.forms import LoginForm, RegisterForm

app = Flask(__name__)

# TODO: change to some valid secret key (this is required by wtf_forms csrf protection)
app.secret_key = b'TODO_CHANGE'


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('login.html', form=form)
    else:
        # TODO: redirect to main page if successful
        return request.form


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        form = RegisterForm()
        return render_template('register.html', form=form)
    else:
        # TODO: redirect to login if valid
        return request.form


if __name__ == '__main__':
    app.run(debug=True)
