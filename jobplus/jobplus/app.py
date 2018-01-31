#coding:utf-8
from flask import Flask
from flask_migrate import Migrate
from jobplus.config import configs
from jobplus.models import db, User
from flask_login import LoginManager
from datetime import datetime

def create_app(config):
	app = Flask(__name__)
	app.config.from_object(configs.get(config))

	register_extensions(app)
	regsiter_blueprints(app)
	register_filters(app)
	return app


def regsiter_blueprints(app):
	from .handlers import front, admin, company, admin, user, job
	app.register_blueprint(front)
	app.register_blueprint(admin)
	app.register_blueprint(company)
	app.register_blueprint(job)
	app.register_blueprint(user)


def register_extensions(app):
	db.init_app(app)
	Migrate(app, db)
	login_manager = LoginManager()
	login_manager.init_app(app)
	@login_manager.user_loader
	def user_loader(id):
		return User.query.get(id)

	login_manager.login_view = 'front.login'



def register_filters(app):
	@app.template_filter()
	def timesince(time):
		now = datetime.utcnow()
		timedelta = now - time
		if timedelta.days > 365:
			return '一年前'
		elif timedelta.days > 30:
			return '{}月前'.format(timedelta.days // 30)
		elif timedelta.days >1:
			return '{}天前'.format(timedelta.days)
		elif timedelta.seconds > 3600:
			return '{}小时前'.format(timedelta.seconds // 3600)
		elif timedelta.seconds > 60:
			return '{}分钟前'.format(timedelta.seconds // 60)
		else:
			return '刚刚'
