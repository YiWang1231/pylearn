from datetime import datetime
from pymongo import MongoClient
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOADS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:wangyi@localhost:3306/tags'
mongo = MongoClient('127.0.0.1', 27017).tags
db = SQLAlchemy(app)


class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category')
    content = db.Column(db.Text)

    def __init__(self, title, created_time, category, content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content

    def __repr__(self):
        return '<File(title=%s)>' % self.title

    def add_tag(self, tag_name):
        file_item = mongo.files.find_one({'file_id': self.id})
        if file_item:
            tags = file_item['tags']
            if tag_name not in tags:
                tags.append(tag_name)
            mongo.files.update_one({'file_id': self.id}, {'$set': {'tags': tags}})
        else:
            tags = [tag_name]
            mongo.files.insert_one({'file_id': self.id, 'tags': tags})
        return tags

    def remove_tag(self, tag_name):
        file_item = mongo.files.find_one({'file_id': self.id})
        if file_item:
            tags = file_item['tags']
            try:
                tags.remove(tag_name)
                new_tags = tags
            except ValueError:
                return tags
            mongo.files.update_one({'file_id': self.id}, {'$set', {'tags': new_tags}})
            return new_tags
        return []

    @property
    def tags(self):
        file_item = mongo.files.find_one({'file_id': self.id})
        if file_item:
            print(file_item)
            return file_item['tags']
        else:
            return []

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    files = db.relationship('File')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return'<Category(name=%s)>' % self.name


# FLASK_APP = app.py flask shell
# form app import db
# db.create_all()
# form app import insert_data()
# insert_data()
def insert_data():
    java = Category('Java')
    python = Category('Python')
    file1 = File('Hello Java', datetime.utcnow(), java, 'File Content - Java is cool!')
    file2 = File('Hello Python', datetime.utcnow(), python, 'File Content - Python is cool!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()
    file1.add_tag('tech')
    file1.add_tag('java')
    file1.add_tag('linux')
    file2.add_tag('tech')
    file2.add_tag('python')


@app.route('/')
def index():
    return render_template('index.html', files=File.query.all())


@app.route('/files/<file_id>')
def file(file_id):
    # file_item = File.query.filter(File.id == file_id).first()
    # if file_item == None:
    # 	abort(404)
    file_item = File.query.get_or_404(file_id)
    return render_template('file.html', file_item=file_item)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(port=3000)
