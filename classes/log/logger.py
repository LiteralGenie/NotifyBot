from copy import copy
import logging.config
import utils, logging, asyncio


class Logger:
	CONFIG= utils.load_yaml(utils.LOGGING_CONFIG)
	logging.config.dictConfig(CONFIG)

	# subclasses should init with: super().__init__(__name__)
	def __init__(self, name):
		self._logger= logging.getLogger(name)
		self._logger._tags= []
		self.template_tags= []
		# self.logger= self

	def _log(self, level, msg, *args, tags=None, **kwargs):
		if not msg:
			return

		# make a copy of current tags
		old= copy(self.tags)

		# add new tags
		self.tags+= self._to_list(tags) + self._to_list(self.template_tags)

		# do log
		self._logger.log(level, msg, *args, **kwargs)

		# revert to initial tags
		self.tags= old
		self.template_tags= []

	def debug(self, *args, **kwargs):
		self._log(logging.DEBUG, *args, **kwargs)
	def info(self, *args, **kwargs):
		self._log(logging.INFO, *args, **kwargs)
	def warning(self, *args, **kwargs):
		self._log(logging.WARNING, *args, **kwargs)
	def error(self, *args, **kwargs):
		self._log(logging.ERROR, *args, **kwargs)
	def critical(self, *args, **kwargs):
		self._log(logging.CRITICAL, *args, **kwargs)

	@property
	def tags(self):
		return self._logger._tags
	@tags.setter
	def tags(self, vals):
		self._logger._tags= self._to_list(vals)
	def append_tag(self, tag):
		old= self.tags
		if tag:
			self.tags= tag
		self.tags= old + self.tags
		return self

	@staticmethod
	def _to_list(vals):
		if vals is None:
			return []

		if not isinstance(vals, list):
			vals= [vals]
		return [x.lower() for x in vals if x]

	def render_template(self, name, dct=None, **kwargs):
		# inits
		if dct is None:
			dct= {}
		dct.update(kwargs)

		name= name.lower()
		TEMPLATES= utils.load_yaml(utils.LOG_STRINGS)

		# add tag
		self.template_tags.append(name.replace("_template",""))

		# get template name
		if not name.endswith("_template"):
			name+= "_template"

		# render
		return utils.render(TEMPLATES[name], dct)

	# add temporary log tag for duration of wrapped function execution
	@classmethod
	def add_tags(cls, tags):
		def decorator(function):
			def wrapper(self, *args, **kwargs):
				old= copy(self.tags)
				self.tags+= cls._to_list(tags)

				result= function(self, *args, **kwargs)

				self.tags= old
				return result
			return wrapper
		return decorator

def log_func(tags=None):
	def decorator(func):
		# if asyncio.iscoroutine(func):
		# 	class LogFunc(Logger):
		# 		def __init__(self):
		# 			self.func= func
		# 			super().__init__(__name__)
		# 			self.tags= self._to_list(tags)
		#
		# 		async def __call__(self, *args, **kwargs):
		# 			return await self.func(self, *args, **kwargs)
		#
		# else:
		class LogFunc(Logger):
			def __init__(self):
				self.func= func
				super().__init__(__name__)
				self.tags= self._to_list(tags)

			def __call__(self, *args, **kwargs):
				return self.func(self, *args, **kwargs)

		return LogFunc()
	return decorator