import ldap
from flask import request, render_template, flash, redirect, url_for, \
    Blueprint, g
from flask_login import current_user, login_user, logout_user, \
    login_required
from flaskipa.forms import LoginForm
from flaskipa.models import User
from flaskipa.utils import redirect_back

auth_bp = Blueprint('auth', __name__)


@auth_bp.before_request
def get_current_user():
    g.user = current_user


@auth_bp.route('/')
@auth_bp.route('/home')
def home():
    return render_template('home.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('auth.home'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            User.try_login(username, password)
        except ldap.INVALID_CREDENTIALS:
            flash('Invalid username or password. Please try again.', 'danger')
            return render_template('login.html', form=form)
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
        login_user(user)
        flash('You have successfully logged in.', 'success')
        return redirect(url_for('auth.home'))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
