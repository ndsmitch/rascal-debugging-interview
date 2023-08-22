from os import environ
from wsgiref.simple_server import make_server

import falcon
import requests
import structlog

from config import Config
from middleware import LoggingMiddleware
from physics import cool

log = structlog.get_logger()
api_key = environ["API_KEY"]


class CoolResource:
    def on_post(self, req, resp):
        """Handles POST request to cool the Ontarian Manifold"""
        api_key = environ["API_KEY"]
        header_key = req.get_header("X-API-Key")
        if header_key != api_key:
            raise falcon.HTTPUnauthorized(description="Invalid API key")

        cool()

        resp.content_type = falcon.MEDIA_TEXT
        resp.text = "COOLED"


class DiagnosticResource:
    def on_get(self, req, resp):
        """Handles GET request for full system diagnostics"""
        api_key = environ["API_KEY"]
        header_key = req.get_header("X-API-Key")
        if header_key != api_key:
            raise falcon.HTTPUnauthorized(description="Invalid API key")

        with open(Config.OntarianManifold.path, "r") as manifold_file:
            ontarian_manifold = manifold_file.read().splitlines()[-1]

        resp.content_type = falcon.MEDIA_TEXT
        resp.text = ontarian_manifold


class HealthCheckResource:
    def on_get(self, req, resp):
        rid = req.get_header("X-Request-ID")
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = rid


if __name__ == '__main__':
    log.info("Booting up the Ramistat Core")

    # Application
    app = falcon.App(middleware=[LoggingMiddleware(log)])

    # Exceptions
    def log_errors(req, resp, ex, params):
        log.error("Unhandled Exception", exc_info=ex)
        raise ex
    app.add_error_handler(Exception, log_errors)
    app.add_error_handler(falcon.HTTPError, log_errors)


    # Resource Mapping
    app.add_route("/cool", CoolResource())
    app.add_route("/diagnostic", DiagnosticResource())
    app.add_route("/healthcheck", HealthCheckResource())

    port = Config.RamistatCore.port
    with make_server('', port, app) as httpd:
        log.info(f"Serving on port {port}...")
        httpd.serve_forever()
