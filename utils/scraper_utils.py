from classes.log.logger import Logger, log_func


def get_session():
	import aiohttp

	# keep-alive because https://github.com/aio-libs/aiohttp/issues/3904#issuecomment-632661245
	return aiohttp.ClientSession(headers={'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'})



@log_func("visit")
async def get_html(logger, link, session=None):
	from classes.errors import TemplatedError

	if session is None:
		session= get_session()


	resp= await session.get(link)
	logger.info(f'Visiting {link}')

	if not resp.status == 200:
		raise TemplatedError("bad_response", link=link, response=resp)
	else:
		text= await resp.text(encoding='utf-8', errors='ignore')
		return text