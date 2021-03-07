import flask

class Server(flask.Flask):
    """Provides wrapper around Flask application allowing services to 
    easily declare public and access-controlled server endpoints using
    the `public_endpoint` and `admin_endpoint` function decorators,
    respectively"""

    # TODO: Implement Server class
