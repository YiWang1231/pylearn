#coding:utf-8
from flask import Blueprint, render_template, redirect, flash, request, current_app, url_for
from jobplus.forms import JobForm, UserForm, Com_RegisterForm, EditCompanyForm, User_RegisterForm
from jobplus.models import Job, User, Company, db
from flask_login import login_required, current_user
from sqlalchemy import desc
admin = Blueprint('admin', __name__, url_prefix="/admin")

@admin.route('/user', methods=['GET','POST'])
@login_required
def user():
	page = request.args.get('page', default=1, type=int)
	pagination = User.query.filter_by().paginate(
		page=page,
		per_page=current_app.config['INDEX_PER_PAGE'],
		error_out=False
		)
	return render_template('admin/user.html', pagination=pagination)

@admin.route('/user/<int:user_id>/edit', methods=['GET','POST'])
@login_required
def user_edit(user_id):
	user = User.query.get_or_404(user_id)
	if user.role == 20:
		form = EditCompanyForm(
			username=user.username,
			email=user.email,
			password=user.password,
			name=user.company.name,
			address=user.company.address,
			logo_url=user.company.logo_url,
			website=user.company.website,
			Slogan=user.company.Slogan,
			description=user.company.description
		)
		if form.validate_on_submit():
			form.update_company(user.company)
			form.update_user(user)
			return redirect(url_for('admin.user'))
	else:
		form = UserForm(obj=user)
		if form.validate_on_submit():
			form.update_user(user)
			return redirect(url_for('admin.user'))
	return render_template('admin/edit_user.html', form=form, user=user)

@admin.route('/user/create', methods=['GET','POST'])
@login_required
def user_create():
	form = User_RegisterForm()
	if form.validate_on_submit():
		form.create_user()
		return redirect(url_for('admin.user'))
	return render_template('admin/create_user.html', form=form)


@admin.route('/company/create', methods=['GET','POST'])
@login_required
def company_create():
	form = Com_RegisterForm()
	if form.validate_on_submit():
		form.create_user()
		form.create_company()
		return redirect(url_for('admin.user'))
	return render_template('admin/create_company.html', form=form)

@admin.route('/job', methods=['GET','POST'])
@login_required
def job():
	page = request.args.get('page', default=1, type=int)
	pagination = Job.query.paginate(
		page=page,
		per_page=current_app.config['INDEX_PER_PAGE'],
		error_out=False
		)
	return render_template('admin/job.html', pagination=pagination)

@admin.route('/job/<int:job_id>/edit', methods=['GET','POST'])
@login_required
def job_edit(job_id):
	job = Job.query.get_or_404(job_id)
	form = JobForm(obj=job)
	if form.validate_on_submit():
		form.update_job(job)
		return redirect(url_for('admin.job'))
	return render_template('admin/edit_job.html', form=form, job=job)


@admin.route('/job/<int:job_id>/open', methods=['GET', 'POST'])
@login_required
def open(job_id):
	job = Job.query.get_or_404(job_id)
	job.is_open = True
	db.session.add(job)
	db.session.commit()
	return redirect(url_for('admin.job'))

@admin.route('/job/<int:job_id>/close', methods=['GET', 'POST'])
@login_required

def close(job_id):
	job = Job.query.get_or_404(job_id)
	job.is_open = False
	db.session.add(job)
	db.session.commit()
	return redirect(url_for('admin.job'))
