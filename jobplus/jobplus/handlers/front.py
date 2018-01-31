#coding:utf-8
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from jobplus.forms import LoginForm, Com_RegisterForm, User_RegisterForm
from jobplus.models import db, User, Company, Job
front = Blueprint('front', __name__)

@front.route('/', methods=['GET', 'POST'])
def index():
	jobs = Job.query.all()[-1:-13:-1]
	companies = Company.query.all()[-1:-13:-1]
	return render_template('index.html', jobs=jobs, companies=companies)

@front.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		login_user(user, form.remember_me.data)
		flash('登陆成功', 'success')
		return redirect(url_for('.index'))
	return render_template('login.html', form=form)

@front.route('/companyregister', methods=["GET", "POST"])
def company_register():
	form = Com_RegisterForm()
	if form.validate_on_submit():
		form.create_user()
		form.create_company()
		flash('注册成功，请登录!', 'success')
		return redirect(url_for('.login'))
	return render_template('company.html', form=form)

@front.route('/userregister', methods=["GET", "POST"])
def user_register():
	form = User_RegisterForm()
	if form.validate_on_submit():
		form.create_user()
		flash('注册成功，请登录!', 'success')
		return redirect(url_for('.login'))
	return render_template('user.html', form=form)


@front.route('/logout')
@login_required
def logout():
	logout_user()
	flash('您已成功退出', 'success')
	return redirect(url_for('.index'))
