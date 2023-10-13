from flask import Blueprint
from flask_login import login_required

options_data_bp = Blueprint("options_data", __name__, template_folder="templates")

# Options data route
@options_data_bp.route("/options")
@login_required
def options():

    return {"page": "options"}