#
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email, EqualTo, Required
from wtforms import ValidationError

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(3, 24)])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('重复密码', validators=[Required(), EqualTo('password')])
    submit = SubmitField('提交')

    def create_user(self):
    	user = User()
    	user.username = self.username.data
    	user.email = self.email.data
    	user.password = self.password.data
    	db.session.add(user)
    	db.session.commit()
    	return user

    def validate_username(self, field):
    	if User.query.filter_by(username=field.data).first():
    		return ValidationError('用户已存在')
    def validate_email(self, field):
    	if User.query.filter_by(email=field.data).first():
    		return ValidationError('邮箱已存在')

class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')
    
    def validate_email(self, field):
    	if field.data and not User.query.filter_by(email=field.data).first():
    		return ValidationError('邮箱未注册')

    def validate_password(self, field):
    	user = User.query.filter_by(email=self.email.data).first()
    	if field.data and not user.checl_password(field.data):
    		return ValidationError('密码错误')