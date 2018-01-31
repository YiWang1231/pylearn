#coding:utf-8
from flask import Blueprint, render_template, redirect, flash, url_for
from jobplus.models import db, User, Delivery, Job, user_job
from jobplus.forms import UserForm, SubResumeForm
from flask_login import login_required, current_user
user = Blueprint('user', __name__, url_prefix="/user")

@user.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	user = User.query.get_or_404(current_user.id)
	form = UserForm(obj=user)
	if form.validate_on_submit():
		form.update_user(user)
		flash('保存成功', 'success')
		return redirect(url_for('user.profile'))
	return render_template('user/profile.html', form=form)

@user.route('/resume', methods=['GET', 'POST'])
@login_required
def resume():
	user = User.query.get_or_404(current_user.id)
	form = SubResumeForm()
	if form.validate_on_submit():
		form.update_user(user)
		flash('简历上传成功', 'success')
		return redirect(url_for('user.profile'))
	return render_template('user/resume.html', form=form)

@user.route('/application')
@login_required

def application():
	delivery = Delivery.query.filter_by(user_id=current_user.id)
	# jobs = db.session.query(Job).join(user_job).filter(user_job.c.user_id==current_user.id)
	jobs = current_user.collect_jobs

	return render_template('user/application.html', deliveries=delivery, jobs=jobs)
