from mako.lookup import TemplateLookup
import os


# todo: automatic lookup creation / rendering function
TEMPLATE_DIR= os.path.join(os.path.dirname(__file__), "templates") + os.sep
LOOKUP= TemplateLookup(directories=[TEMPLATE_DIR])


from .urls import bp