from datetime import datetime
from functools import wraps #用来返回原函数的名字的

def log(func):
	@wraps(func)#不改变原函数的名字
	def decorator(*args, **kwargs):
		print('Function ' + func.__name__ + ' has been called at '+ datetime.now().strftime('%Y-%m_%d  %H:%M:%S'))
		return func(*args, **kwargs)
	return decorator


@log
def add(x, y):
	return x+y


if __name__ == "__main__":

	add(1,2)