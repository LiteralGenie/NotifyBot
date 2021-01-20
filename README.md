# NotifyBot

Discord bot for pulling updates from various websites.

## Setup

1. Clone this repo. `git clone https://github.com/LiteralGenie/NotifyBot`

2. Create a `config/bot_config.json` file using the example config.

3. Install requirements. `pip install -r requirements.txt`

4. Run `main.py`.

## Adding a new update feed

1. Create a class that contains a `get_update()` function. The function should return an iterable that yields a dictionary contaning kwargs suited for discordpy's [`Messagable.send()`](https://discordpy.readthedocs.io/en/latest/api.html#discord.abc.Messageable.send) function. 
     - Alternatively, subclass the `classes.scrapers.UpdateScraper` class and override the `parse_update_page` and `parse_series_page` functions.

2. Add the class to the `__init__` function in `cogs/update_cog.py`.

3. Edit the `config/mentions.yaml` and `config/series_blacklist.yaml` file as necessary. The mako template for existing update feeds can be edited in `templates/updates.yaml`.

A partial example...

```py
# cogs/update_cog.py
from classes.scrapers import MyScraper

class UpdateCog(...):
    def __init__(self, bot):
	      ... # initialize supers and other instance vars

        update_channel= self.bot.get_channel(channel_id)
        self.get_loop(ScraperClass=MyScraper, name='id_for_config_stuff', out_channel=update_channel).start()

    # handles the timer checks and message sending
    def get_loop(self, name, ScraperClass, out_channel):
        ... 

# classes/scrapers/my_scraper.py
class MyScraper:
    @classmethod
    async def get_updates(cls):
        updates= ... # get list of updates
        
        async for x in updates:
            yield dict(content= f"new update for {x.name}!")
```


----

Example of an update feed:

<img src=https://files.catbox.moe/rmbi0q.png></img>
