from flask import Blueprint, render_template, flash, redirect,url_for
from simpledu.models import Course, db, User
from simpledu.froms import RegisterForm, LoginForm
from flask_login import login_user, login_required

front = Blueprint('front', __name__)

@front.route('/')
def index():
	courses = Course.query.all()
	return render_template('index.html', courses=courses)

@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出成功', 'success')
    return redirect(url_for('.index'))

@front.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)

