#coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, IntegerField ,SelectField
from wtforms.validators import Length, Email, EqualTo, Required, URL, NumberRange
from flask_wtf.file import FileField, FileRequired
from jobplus.models import db, User, Job, Company
from flask_login import current_user
import os
from flask import url_for

class LoginForm(FlaskForm):
	email = StringField('邮箱', validators=[Required(), Email()])
	password = PasswordField('密码', validators=[Required(), Length(6, 24)])
	remember_me = BooleanField('记住我')
	submit = SubmitField('提交')

	def validate_email(self, field):
		if field.data and not User.query.filter_by(email=field.data).first():
			raise 	ValidationError('该邮箱未注册')

	def  validate_password(self, field):
		user = User.query.filter_by(email=self.email.data).first()
		if user and not user.check_password(field.data):
			raise ValidationError('密码错误')


class Com_RegisterForm(FlaskForm):
	username = StringField('用户名', validators=[Required(), Length(3,24)])
	email = StringField('邮箱', validators=[Required(), Email()])
	password = PasswordField('密码', validators=[Required(), Length(3, 24)])
	repeat_password = PasswordField('重复密码', validators=[Required(), EqualTo('password')])
	name = StringField('公司名称', validators=[Required()])
	submit = SubmitField('提交')


	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('该用户名已存在')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('邮箱已存在')

	def create_user(self):
		user = User()
		self.populate_obj(user)
		user.role = 20
		user.company = Company(name=self.name.data)
		db.session.add(user)
		db.session.commit()

		return user

	def create_company(self):
		company = Company(name=self.name.data)

		db.session.add(company)
		db.session.commit()
		return company



class User_RegisterForm(FlaskForm):
	username = StringField('用户名', validators=[Required(), Length(3,24)])
	email = StringField('邮箱', validators=[Required(), Email()])
	password = PasswordField('密码', validators=[Required(), Length(3, 24)])
	repeat_password = PasswordField('重复密码', validators=[Required(), EqualTo('password')])
	realname = StringField('真实姓名', validators=[Required()])
	submit = SubmitField('提交')


	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('该用户名已存在')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('邮箱已存在')

	def create_user(self):
		user = User()
		self.populate_obj(user)
		db.session.add(user)
		db.session.commit()

		return user


class CompanyForm(FlaskForm):
	"""docstring for CompanyForm"""
	name = StringField('公司名称', validators=[Required(), Length(1, 128)])
	address = StringField('地址',validators=[Required(), Length(1,128)])
	logo_url = StringField('Logo URL',validators=[Required()])
	website = StringField('官网', validators=[Required()])
	Slogan = StringField('口号', validators=[Required(),Length(1,1024)])
	description = StringField('描述', validators=[Required(), Length(1,1024)])

	submit = SubmitField('保存')

	def update_company(self, company):
		self.populate_obj(company)
		db.session.add(company)
		db.session.commit()
		return company

class JobForm(FlaskForm):
	name = StringField('职位名称', validators=[Required()])
	salary_low = StringField('最低工资', validators=[Required()])
	salary_high = StringField('最高工资', validators=[Required()])
	address = StringField('地址', validators=[Required(), Length(1, 256)])
	degree_request = StringField('学历要求', validators=[Required()])
	exp_request = StringField('经验要求', validators=[Required()])
	tags = StringField('标签（用多个，隔开）')
	job_request = StringField('工作要求，用逗号隔开', validators=[Required()])
	is_open = BooleanField('是否上线')
	is_fulltime = BooleanField('是否全职')
	submit = SubmitField('添加')


	def create_job(self):
		job = Job()
		self.populate_obj(job)
		job.company_id = current_user.company.id
		db.session.add(job)
		db.session.commit()
		return job


	def update_job(self, job):
		self.populate_obj(job)
		db.session.add(job)
		db.session.commit()
		return job


class UserForm(FlaskForm):

	username = StringField('用户名', validators=[Required(), Length(1, 32)])
	email = StringField('邮箱', validators=[Required(),Email()])
	password = PasswordField('密码，不输入默认不变')
	realname = StringField('真实姓名', validators=[Required(), Length(1, 24)])
	phone = StringField('手机号码')
	work_years = IntegerField('工龄')
	education = SelectField('选择学历',
		choices=[
		('不限', '不限'),
		('本科', '本科'),
		('硕士', '硕士'),
		('博士','博士')
		])
	description = TextAreaField('个人简介')
	resume_url = StringField('简历链接')
	submit = SubmitField('保存')


	def validate_phone(self, field):
		if field.data[:2] not in ('13', '15', '18') and len(field.data) != 11:
			return ValidationError('请输入有效手机号')

	def update_user(self, user):
		self.populate_obj(user)
		db.session.add(user)
		db.session.commit()
		return user

class SubResumeForm(FlaskForm):
	resume = FileField('简历上传', validators=[FileRequired()])
	submit = SubmitField('提交')

	def upload_resume(self):
		f = self.resume.data
		filename = current_user.realname + '.pdf'
		# dirname 获得文件路径 / jobplus
		f.save(os.path.join(
			os.path.abspath(os.path.dirname(__file__)),
			'static',
			'resumes',
			filename
			))
		return filename
	def update_user(self, user):
		filename = self.upload_resume()
		user.resume_url = url_for('static', filename=os.path.join('resumes', filename))
		db.session.add(user)
		db.session.commit()


class EditCompanyForm(FlaskForm):
	"""docstring for CompanyForm"""
	username = StringField('用户名', validators=[Required()])
	email = StringField('邮箱', validators=[Required(), Email()])
	password = PasswordField('密码')
	name = StringField('公司名称', validators=[Required(), Length(1, 128)])
	address = StringField('地址',validators=[Required(), Length(1,128)])
	logo_url = StringField('Logo URL',validators=[Required()])
	website = StringField('官网', validators=[Required()])
	Slogan = StringField('口号', validators=[Required(),Length(1,1024)])
	description = StringField('描述', validators=[Required(), Length(1,1024)])
	submit = SubmitField('保存')


	def update_company(self, company):
		self.populate_obj(company)
		db.session.add(company)
		db.session.commit()
		return company

	def update_user(self, user):
		self.populate_obj(user)
		db.session.add(user)
		db.session.commit()
		return user