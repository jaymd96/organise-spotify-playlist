from flask import Blueprint, redirect, url_for, session
import views.web as web

static_bp = Blueprint(
    name="static_bp",
    import_name=__name__,
    static_folder="../dist",
    static_url_path="",
)


@static_bp.route("/")
def index():
    return redirect("/api")
    # return web.redirect(url_for(".static", filename="index.html"))
