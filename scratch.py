def get_decorator(tags=None):
	def decorator(func):
		class wrapper:
			def __init__(self):
				print('init')
				self.func= func

			def __call__(self):
				print('call')
				print(tags)
				self.func()

		return wrapper()
	return decorator

@get_decorator(tags='1')
def p():
	print('hi')

p()
