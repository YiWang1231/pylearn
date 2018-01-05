from flask import Flask, render_template
from simpledu.config import configs
from simpledu.models import db, Course, User 
from flask_migrate import Migrate
from flask_login import LoginManager

def create_app(config):
	app = Flask(__name__)
	app.config.from_object(configs.get(config))
	register_extensions(app)
	register_blueprints(app)
	return app
def register_blueprints(app):
    from .handler import admin, front, user, course
    app.register_blueprint(admin)
    app.register_blueprint(front)
    app.register_blueprint(user)
    app.register_blueprint(course)

def register_extensions(app):
	db.init_app(app)
	Migrate(app, db)
	login_manager = LoginManager()
	login_manager.init_app(app)

	@login_manager.user_loader
	def user_loader(id):
		User.query.get(id)

	login_manager.login_view = 'front.login'