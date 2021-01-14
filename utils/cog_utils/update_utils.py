import time, traceback, utils
from classes.log.logger import log_func


# config should have a key for (key + '_check_frequency_seconds')
def update_check(key, self):
	def decorator(func):
		async def wrapper():
			# check for updates periodically
			do_update= True

			# dont use loop.current_loop because this decorator must be before @tasks.loop
			# if self.check_sushi.current_loop != 0:
			if self.iterations.get(key, 0) != 0:
				last_check= time.time() - self.check_times[key]
				last_check= last_check

				do_update= (last_check >= self.bot.config[key + '_check_frequency_seconds'])

			# send update messages
			if do_update:
				self.check_times[key]= time.time()
				self.iterations[key]= 1 + self.iterations.get(key,0)
				await func()

		return wrapper
	return decorator

def handle_loop_error(self):
	def decorator(func):
		async def wrapper():
			try:
				await func()
			except Exception as e:
				ERROR_STRINGS= utils.load_yaml(utils.ERROR_STRINGS)
				text= "".join(traceback.format_tb(e.__traceback__))

				ret= utils.render(
					ERROR_STRINGS['loop_template'],
					dict(EXCEPTION=text)
					)

				self.error(text, tags=['update loop'])
				await self.update_channel.send(ret)
		return wrapper
	return decorator