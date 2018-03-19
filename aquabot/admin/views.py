from flask import current_app, render_template, request, flash, redirect, url_for
from . import admin
from .forms import LoginForm
from ..models import User
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse


@admin.route('/')
@admin.route('/index')
@login_required
def index():
    return render_template('index.html', title="aquabot")


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # Return with registration
        # if user is None or not user.check_password(form.password.data):
        if user is None:
            flash('Invalid username or password')
            return redirect(url_for('.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)
