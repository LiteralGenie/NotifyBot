from discord.ext import commands
from discord.errors import Forbidden
from .templated_error import TemplatedError

import utils, traceback, sys

# mixin for globally handling errors
class ErrorHandler:
	async def on_command_error(self, ctx, e):
		if isinstance(e, TemplatedError):
			return await ctx.send(e.render(ctx))
		else:
			return await self.handle_other_error(ctx, e)

	# Unexpected errors
	async def handle_other_error(self, ctx, e):
		# get the actual stack trace if available
		if isinstance(e, commands.CommandInvokeError):
			err= e.original
		else: err= e

		# dump into template
		ERROR_STRINGS= utils.load_yaml(utils.ERROR_STRINGS)
		text= "\n".join(traceback.format_tb(err.__traceback__)) + "\n---\n" + str(e)
		uncaught= utils.render(ERROR_STRINGS['uncaught_template'], dict(EXCEPTION=text[-1400:], MESSAGE=ctx.message.content[:400]))

		# print
		await ctx.send(uncaught)
		traceback.print_tb(err.__traceback__)
		sys.stderr.write(str(e))