#coding:utf-8
from flask import Blueprint, render_template, redirect, url_for, current_app, flash, request
from jobplus.models import db, Job, User, Delivery
from flask_login import login_required, current_user, current_user
from datetime import datetime
from jobplus.forms import JobForm

job = Blueprint('job', __name__, url_prefix="/job")

@job.route('/')

def index():
	page = request.args.get('page', default=1, type=int)
	pagination = Job.query.order_by(Job.create_at.desc()).paginate(
		page=page,
		per_page=current_app.config['INDEX_PER_PAGE'],
		error_out=False
		)
	return render_template('job/index.html', pagination=pagination)


@job.route('/admin')
@login_required
def admin():
	page = request.args.get('page', default=1, type=int)
	pagination = Job.query.filter_by(company_id=current_user.company.id).paginate(
		page=page,
		per_page=current_app.config['INDEX_PER_PAGE'],
		error_out=False
		)
	return render_template('job/admin.html', pagination=pagination)


@job.route('/new', methods=['GET', 'POST'])
@login_required
def new():
	form = JobForm()
	if form.validate_on_submit():
		form.create_job()
		return redirect(url_for('job.admin'))
	return render_template('job/create_job.html', form=form)


@job.route('/<int:job_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
	job = Job.query.get_or_404(job_id)
	form = JobForm(obj=job)
	if form.validate_on_submit():
		form.update_job(job)
		return redirect(url_for('job.admin'))
	return render_template('job/edit_job.html', form=form, job=job)

@job.route('/<int:job_id>/open', methods=['GET', 'POST'])
@login_required

def open(job_id):
	job = Job.query.get_or_404(job_id)
	job.is_open = True
	db.session.add(job)
	db.session.commit()
	return redirect(url_for('job.admin'))

@job.route('/<int:job_id>/close', methods=['GET', 'POST'])
@login_required

def close(job_id):
	job = Job.query.get_or_404(job_id)
	job.is_open = False
	db.session.add(job)
	db.session.commit()
	return redirect(url_for('job.admin'))


@job.route('/<int:job_id>')
@login_required
def job_detail(job_id):
	job = Job.query.get_or_404(job_id)
	tags = job.tags.split('，')
	job_request = job.job_request.split('，')
	return render_template('job/detail.html', job=job, tags=tags, job_request=job_request)


@job.route('/<int:job_id>apply')
@login_required

def apply(job_id):
	user = current_user
	job = Job.query.get_or_404(job_id)
	user.collect_jobs.append(job)
	delivery = Delivery(
	job_id=job_id,
	user_id=user.id,
	company_id=job.company.id,
	job_name = job.name,
	user_realname=user.realname,
	job_address=job.address
	)
	db.session.add(delivery)
	db.session.add(user)
	db.session.commit()
	return redirect(url_for('job.job_detail', job_id=job_id))
