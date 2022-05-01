import dotenv
import os

env = dotenv.load_dotenv()

from flask import Flask
from flask_cors import CORS
from flask_session import Session

from views.api import api_bp
from views.vue import static_bp


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SESSION_TYPE"] = os.getenv("SESSION_TYPE")
app.config["SESSION_FILE_DIR"] = os.getenv("SESSION_FILE_DIR")

app.register_blueprint(api_bp)
app.register_blueprint(static_bp)

CORS(
    app,
)
Session(app)


"""
Following lines allow application to be run more conveniently with
`python app.py` (Make sure you're using python3)
(Also includes directive to leverage pythons threading capacity.)
"""
if __name__ == "__main__":
    app.run(
        threaded=True,
        port=int(os.environ.get("PORT", 8888)),
    )
