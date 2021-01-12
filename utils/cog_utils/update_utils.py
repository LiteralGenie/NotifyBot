import time

# config should have a key for (key + '_check_frequency_minutes')
def update_check(key):
	def decorator(func):
		async def wrapper(self):
			# check for updates periodically
			do_update= True

			# dont use loop.current_loop because this decorator must be before @tasks.loop
			# if self.check_sushi.current_loop != 0:
			if self.iterations.get(key, 0) != 0:
				last_check= time.time() - self.check_times[key]
				last_check= last_check / 60

				do_update= (last_check >= self.bot.config[key + '_check_frequency_minutes'])

			# send update messages
			if do_update:
				self.check_times[key]= time.time()
				self.iterations[key]= 1 + self.iterations.get(key,0)
				await func(self)

		return wrapper
	return decorator