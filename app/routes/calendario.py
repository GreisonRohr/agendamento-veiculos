from flask import (
    Blueprint,
    jsonify,
    render_template
)

from app.services.calendario_service import CalendarioService
from app.services.auth_service import login_required


calendario_bp = Blueprint(
    "calendario",
    __name__,
    url_prefix="/calendario"
)


@calendario_bp.route("/")
@login_required
def index():

    return render_template(
        "calendario/index.html"
    )


@calendario_bp.route("/eventos")
@login_required
def eventos():

    return jsonify(
        CalendarioService.eventos()
    )
