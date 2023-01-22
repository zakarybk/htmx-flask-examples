import json
from flask import Flask, render_template, Response
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect

from .models import User
from .forms import LoginForm

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY="secret_sauce",
)

login_manager = LoginManager()
login_manager.init_app(app)

csrf = CSRFProtect()
csrf.init_app(app)


@login_manager.user_loader
def load_user(user_id: str) -> User:
    return User(name=user_id)


@app.route("/")
def index():
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login() -> Response:
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(User(form.name.data), remember=form.remember_me.data)

        return Response(status=204, headers={'HX-Trigger': json.dumps({'loginUpdate': None})})

    return render_template('modals/login.html', form=form)


@app.route('/login-btn', methods=['GET'])
def login_btn():
    return render_template('components/login_btn.html')


@app.route("/logout")
@login_required
def logout() -> Response:
    logout_user()
    return Response(status=204, headers={'HX-Trigger': 'loginUpdate'})
