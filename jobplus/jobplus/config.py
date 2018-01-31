#coding:utf-8
class BaseConfig(object):
	SECRET_KEY = 'OENDA YOUWILLBE A AMAZING PYTHONENGINEER'
	INDEX_PER_PAGE = 9

class DevelopementConfig(BaseConfig):
	DEBUG=True
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:wangyi@localhost:3306/jobplus?charset=utf8'

class ProductionConfig(BaseConfig):
	DEBUG=False

class TestingConfig(BaseConfig):
	DEBUG=False


configs = {
	'develope':DevelopementConfig,
	'product': ProductionConfig,
	'test': TestingConfig
}
