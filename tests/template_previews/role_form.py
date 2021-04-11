from mako.template import Template
from mako.lookup import TemplateLookup
import utils


roles= dict(
	test="1234",
	a=[123,43,"3s22"]
)

template_dir= utils.WEBVIEW_DIR + "settings/templates/"
print(template_dir)
lookup= TemplateLookup(directories=[template_dir])

template= Template(
	filename=template_dir + "index.html",
	lookup=lookup
)
print(template.render(ROLES=roles))