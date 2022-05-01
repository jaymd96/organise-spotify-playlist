from flask import Blueprint, redirect, url_for, session

static_bp = Blueprint(
    name="static_bp",
    import_name=__name__,
    static_folder="../dist",
    static_url_path="",
)


@static_bp.route("/")
def index():
    if session.get("uuid"):
        return redirect("/index.html#/go")
    return redirect(url_for("static", filename="index.html"))
