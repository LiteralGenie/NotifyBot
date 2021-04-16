from quart import Blueprint
from . import views


bp= Blueprint("settings", __name__)
bp.add_url_rule("/settings/", view_func=views.SettingsView.as_view("index"))
bp.add_url_rule("/settings/roles", view_func=views.RoleView.as_view("role_post"))