from discord.ext import ipc, commands

# defines routes for the IPC server
class WebviewCog(commands.Cog):
	def __init__(self, bot):
		super().__init__()
		self.bot= bot

	@ipc.server.route()
	async def get_available_roles(self, data):
		roles= []
		for g in self.bot.guilds:
			roles+= g.roles
		return { r.id: r.name for r in roles }

	@ipc.server.route()
	async def ping(self, _):
		import time
		return time.time_ns()