from flask import Flask, render_template, abort
import os
import json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

directory = os.path.join(os.path.abspath(os.path.dirname(__name__)), '..', 'files')


def read_files(directory):
	result = {}
	for file in os.listdir(directory):
		filepath = os.path.join(directory, file)
		with open(filepath, 'r') as f:
			result[file[:-5]] = json.load(f)
	return result


def get_title(directory):
	files_dict = read_files(directory)
	return [item['title'] for item in files_dict.values()]


def get_filename(directory, filename):
	files_dict = read_files(directory)
	return files_dict.get(filename)
		

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'),404


@app.route('/')
def index():
	return render_template('index.html', title_list=get_title(directory))


@app.route('/files/<filename>')
def file(filename):
	file_item = get_filename(directory, filename)
	if not file_item:
		abort(404)
	return render_template('file.html', file_item=file_item)
