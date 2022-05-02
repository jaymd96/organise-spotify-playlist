import flask
import os


def redirect(*args, **kwargs):
    prefix = os.getenv("LOCAL_CLIENT_URL", "")
    return flask.redirect(prefix + args[0], *args[1:], **kwargs)
