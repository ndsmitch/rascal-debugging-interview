from os import environ
from wsgiref.simple_server import make_server

import falcon
import requests
import structlog

from config import Config
from middleware import LoggingMiddleware
from physics import warp

log = structlog.get_logger()


class WarpResource:
    def on_put(self, req, resp):
        """Handles PUT request to warp locations"""
        api_key = environ["API_KEY"]
        header_key = req.get_header("X-API-Key")
        if header_key != api_key:
            raise falcon.HTTPUnauthorized(description="Invalid API key")

        location = req.get_media()["location"]
        warp(location)

        resp.status = 200
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = "OK"


class DiagnosticResource:
    def on_get(self, req, resp):
        """Handles GET request for full system diagnostics"""
        api_key = environ["API_KEY"]
        header_key = req.get_header("X-API-Key")
        if header_key != api_key:
            raise falcon.HTTPUnauthorized(description="Invalid API key")

        with open(Config.Location.path, "r") as location_file:
            location = location_file.read().splitlines()[-1]

        resp.status = 200
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = location


class HealthCheckResource:
    def on_get(self, req, resp):
        rid = req.get_header("X-Request-ID")
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = rid


if __name__ == '__main__':
    log.info("Booting up the Firomactal Drive")

    # Application
    app = falcon.App(middleware=[LoggingMiddleware(log)])

    # Exceptions
    def log_errors(req, resp, ex, params):
        log.error("Unhandled Exception", exc_info=ex)
        raise ex
    app.add_error_handler(Exception, log_errors)
    app.add_error_handler(falcon.HTTPError, log_errors)

    # Resource Mapping
    app.add_route("/warp", WarpResource())
    app.add_route("/diagnostic", DiagnosticResource())
    app.add_route("/healthcheck", HealthCheckResource())

    port = Config.FiromactalDrive.port
    with make_server('', port, app) as httpd:
        log.info(f"Serving on port {port}...")
        httpd.serve_forever()
