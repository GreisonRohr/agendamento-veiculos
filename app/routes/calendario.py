from flask import (
    Blueprint,
    jsonify,
    render_template
)

from app.services.calendario_service import CalendarioService


calendario_bp = Blueprint(
    "calendario",
    __name__,
    url_prefix="/calendario"
)


@calendario_bp.route("/")
def index():

    return render_template(
        "calendario/index.html"
    )


@calendario_bp.route("/eventos")
def eventos():

    return jsonify(
        CalendarioService.eventos()
    )