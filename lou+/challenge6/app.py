from flask import Flask, render_Template
from flask_sqlalchemy import SQLALchemy
from pymomgo import MongoClient
from  datetime import datetime


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:wangyi@localhost:3306/tags'
db = SQLALchemy(app)


mongo = MongoClient('127.0.0.1', 27017).tags


class File(db.Model):
	__tablename__ = 'files'
	id = db.Clomun(db.Integer, primary_key=True)
	title= db.Column(db.String(80))
	created_time = db.Column(db.DateTime)
	category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
	category = db.relationship('Category')
	content = db.Column(db.Text)

	def__init__(self, title, created_time, category, content):
		self.title = title
		self.created_time = created_time
		self.category = category
		self.content = content
	def __repr__(self):
		return '<File(title=%s)>' % self.title

	def add_tag(self, tag_name):
		pass
	def remove_tag(self, tag_name):
		pass

	@property
	def tags(self):
		pass


class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	files = db.relationship('File')

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Category(name=%s)>' % self.name



def insert_data():
	pass


@app.route('/')
def index():
	return render_Template('index.html', files = File.query().all())


@app.route('/files/<file_id>')
