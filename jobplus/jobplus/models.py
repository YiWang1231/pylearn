#coding:utf-8
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
db = SQLAlchemy()

class Base(db.Model):
	__abstract__ = True
	create_at = db.Column(db.DateTime, default=datetime.utcnow)
	update_at = db.Column(db.DateTime,
						  default=datetime.utcnow,
						  onupdate=datetime.utcnow)



user_job = db.Table(
	'user_job',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')),
	db.Column('job_id', db.Integer, db.ForeignKey('job.id', ondelete='CASCADE'))
	)

class User(Base, UserMixin):
	__tablename__ = 'user'

	ROLE_USER = 10
	ROLE_COMPANY = 20
	ROLE_ADMIN = 30

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(32), unique=True, index=True, nullable=False)
	email = db.Column(db.String(64), unique=True, index=True, nullable=False)
	_password = db.Column('password', db.String(256), nullable=False)
	realname = db.Column(db.String(24))
	phone = db.Column(db.String(11))
	role = db.Column(db.SmallInteger, default=ROLE_USER)
	# 求职用户的字段
	work_years = db.Column(db.SmallInteger)
	education = db.Column(db.String(24))
	description = db.Column(db.String(1024))
	resume = db.relationship('Resume', uselist=False)
	collect_jobs = db.relationship('Job', secondary=user_job, backref=db.backref('users'))
	resume_url = db.Column(db.String(64))
	# CASCADE 表示企业如果删除，对应的子账号也要删除
	company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))
	company = db.relationship('Company', uselist=False)

	def __repr__(self):
		return "<User:{}>".format(self.username)

	@property
	def password(self):
		return self._password

	@password.setter
	def password(self, orig_password):
		self._password = generate_password_hash(orig_password)

	def check_password(self, password):
		return check_password_hash(self._password, password)

	@property

	def is_admin(self):
		return self.role == self.ROLE_ADMIN
	@property
	def is_company(self):
		return self.role == self.ROLE_COMPANY
	@property
	def is_user(self):
		return self.role == self.ROLE_USER

class Resume(Base):
	__tablename__ = 'resume'

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', uselist=False)
	job_experience = db.relationship('JobExperience')
	edu_experience = db.relationship('EduExperience')
	project_experience = db.relationship('ProjectExperience')


class Experience(Base):
	__abstract__ = True

	id = db.Column(db.Integer, primary_key=True)
	begin_at = db.Column(db.DateTime)
	end_at = db.Column(db.DateTime)
	#个人工作经历描述
	description = db.Column(db.String(1024))


class JobExperience(Experience):

	__tablename__ = 'job_experience'

	used_company = db.Column(db.String(32), nullable=False)
	city = db.Column(db.String(32), nullable=False)
	resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
	resume = db.relationship('Resume', uselist=False)

class EduExperience(Experience):

	__tablename__ = 'edu_experience'

	school = db.Column(db.String(32), nullable=False)
	major = db.Column(db.String(32), nullable=False)
	degree = db.Column(db.String(16))
	resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
	resume = db.relationship('Resume', uselist=False)

class ProjectExperience(Experience):

	__tablename__ = 'project_experience'

	name = db.Column(db.String(32), nullable=False)
	role = db.Column(db.String(32))
	# 技术用 , 分开
	technologys = db.Column(db.String(64))
	resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
	resume = db.relationship('Resume', uselist=False)



class Job(Base):
	__tablename__ = 'job'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128), unique=True, index=True, nullable=False)
	salary_low = db.Column(db.Integer, nullable=False)
	salary_high = db.Column(db.Integer, nullable=False)
	address = db.Column(db.String(256))
	exp_request = db.Column(db.String(32))
	degree_request = db.Column(db.String(32))
	description = db.Column(db.String(1024))
	job_request = db.Column(db.String(1024))
	tags = db.Column(db.String(128))
	is_fulltime = db.Column(db.Boolean, default=True)
	is_open = db.Column(db.Boolean, default=True)
	view_count = db.Column(db.Integer, default=0)
	company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))
	company = db.relationship('Company', backref=db.backref('job'))



class Company(Base):
	__tablename__ = 'company'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128), unique=True, index=True, nullable=False)
	address = db.Column(db.String(256))
	logo_url = db.Column(db.String(256))
	website = db.Column(db.String(256), default="http://www.kernel.org")
	Slogan = db.Column(db.String(256))
	#一句话描述
	description = db.Column(db.String(100))
	# 详情描述
	about = db.Column(db.String(1024))
	# 标签, 用逗号隔开
	tags = db.Column(db.String(128))
	user=db.relationship('User', uselist=False)


class Delivery(Base):

	__tablename__ = 'delivery'

	# 等待审核
	STATUS_WAITING = 1
	# 被拒绝
	STATUS_REJECT = 2
	# 等通知
	STATUS_ACCEPT = 3

	id = db.Column(db.Integer, primary_key=True)
	job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete='SET NULL'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
	company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='SET NULL'))
	user_realname = db.Column(db.String(32))
	job_name = db.Column(db.String(32))
	job_address = db.Column(db.String(32))
	status = db.Column(db.SmallInteger, default=STATUS_WAITING)
	# 企业回应
	response =  db.Column(db.String(256))
