# NotifyBot

Discord bot for pulling updates from various websites. 

Notably...
- Mangadex (filtered by the user's follows)
- AnimeNewsNetwork
- Genkan-powered sites.

## Setup

1. Clone this repo. `git clone https://github.com/LiteralGenie/NotifyBot`

2. Create a `config/bot_config.json` file using the example config.

3. Install requirements. `pip install -r requirements.txt`

4. Run `main.py`.

## Adding a new update feed

1. Subclass the `classes.scrapers.UpdateScraper` class and override the `parse_update_page` and `parse_series_page` functions. See `classes/scrapers/update_scraper.py` for explanations of what these functions should return. Also refer to the other classes in `classes/scrapers/` for examples.

2. Add a `BLAH_check_frequency_seconds` entry to the `config/bot_config.yaml` file, where `BLAH` can be whatever.

3. Edit the `__init__` function in `cogs/update_cog.py`.
```
class UpdateCog:
    def __init__(self, bot):
        ...
        new_channel= self.bot.get_channel(channel_id) # get from discord app --- right-click channel and "copy id"
	config_key= "BLAH" # used for getting the check frequency
        self.get_loop(config_key, MyScraperClass, new_channel).start()
```

4. Edit the `config/mentions.yaml` and `config/series_blacklist.yaml` file as necessary. The [mako](https://www.makotemplates.org/) template for existing update feeds can be edited in `templates/updates.yaml`.

A partial example...

```py
# cogs/update_cog.py
from classes.scrapers import MyScraper

class UpdateCog(...):
    def __init__(self, bot):
        ...
        update_channel= self.bot.get_channel(channel_id)
        self.get_loop(ScraperClass=MyScraper, name='id_for_config_stuff', out_channel=update_channel).start()

    # handles the timer checks and message sending -- already exists, don't need to create
    def get_loop(self, name, ScraperClass, out_channel):
        ... 

# classes/scrapers/my_scraper.py
class MyScraper:
    @classmethod
    async def get_updates(cls):
        updates= [] # get list of updates
        
        async for x in updates:
            yield dict(content= f"new update for {x.name}!")
```


----

Example of an update feed:

<img src=https://files.catbox.moe/rmbi0q.png></img>
