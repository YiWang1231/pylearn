from flask import Blueprint
from simpledu.models import Course, db, User

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
def admin_index():
	return 'admin'