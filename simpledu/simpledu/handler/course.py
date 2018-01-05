from flask import Blueprint, render_template
from simpledu.models import Course, db

course = Blueprint('course', __name__, url_prefix='/courses')

@course.route('/')
def courses_index():
	return render_template('courses.html')