#coding:utf-8
from flask import Blueprint, render_template, url_for, current_app, flash, redirect, request
from jobplus.models import db, Company, Job, Delivery, User
from flask_login import login_required, current_user
import random
from jobplus.forms import CompanyForm
company = Blueprint('company', __name__, url_prefix="/company")

@company.route('/', methods=['GET', 'POST'])
def index():
	page = request.args.get('page', default=1, type=int)
	pagination = Company.query.paginate(
		page=page,
		per_page=current_app.config['INDEX_PER_PAGE'],
		error_out=False
		)
	num = random.sample(range(0, 30), 30)
	return render_template('company/index.html', pagination=pagination,job_num=num)

@company.route('/<int:company_id>')
def company_detail(company_id):
	company = Company.query.get_or_404(company_id)
	return render_template('company/detail.html', company=company)


@company.route('/admin/profile', methods=['GET', 'POST'])
@login_required
def profile():
	company = Company.query.get_or_404(current_user.company.id)
	form = CompanyForm(obj=company)
	if form.validate_on_submit():
		form.update_company(company)
		return redirect(url_for('company.profile'))
	return render_template('company/profile.html', form=form)


@company.route('/<int:company_id>/jobs')
def company_jobs(company_id):
	company = Company.query.get_or_404(company_id)
	jobs = Job.query.filter_by(company_id=company_id)
	return render_template('company/company_jobs.html', company=company, jobs=jobs)


@company.route('/application/waiting')

def waiting():
	page = request.args.get('page', default=1, type=int)
	pagination = Delivery.query.filter_by(status=1, company_id=current_user.company_id).paginate(
		page=page,
		per_page=current_app.config['INDEX_PER_PAGE'],
		error_out=False
	)
	print(pagination.items)
	return render_template('company/waiting.html', pagination = pagination)



@company.route('/application/accept')

def accept():
	page = request.args.get('page', default=1, type=int)
	pagination = Delivery.query.filter_by(status=3, company_id=current_user.company_id).paginate(
		page=page,
		per_page=current_app.config['INDEX_PER_PAGE'],
		error_out=False
	)
	return render_template('company/accept.html', pagination = pagination)


@company.route('/application/reject')

def reject():
	page = request.args.get('page', default=1, type=int)
	pagination = Delivery.query.filter_by(status=2, company_id=current_user.company_id).paginate(
		page=page,
		per_page = current_app.config['INDEX_PER_PAGE'],
		error_out = False
	)
	return render_template('company/reject.html', pagination = pagination)


@company.route('/delivery/<int:delivery_id>/resume')
def delivery_resume(delivery_id):
	delivery = Delivery.query.get_or_404(delivery_id)
	user = User.query.get(delivery.user_id)
	print(user.resume_url)
	return redirect(user.resume_url)


@company.route('/delivery/<int:delivery_id>/reject')
def delivery_reject(delivery_id):
	delivery = Delivery.query.get_or_404(delivery_id)
	delivery.status = 2
	db.session.add(delivery)
	db.session.commit()
	return redirect(url_for('company.reject'))


@company.route('/delivery/<int:delivery_id>/accept')
def delivery_accept(delivery_id):
	delivery = Delivery.query.get_or_404(delivery_id)
	delivery.status = 3
	db.session.add(delivery)
	db.session.commit()
	return redirect(url_for('company.accept'))