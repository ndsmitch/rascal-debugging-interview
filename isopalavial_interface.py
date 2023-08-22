from os import environ
from wsgiref.simple_server import make_server

import falcon
import requests
import structlog

from clients import (
    FiromactalDriveClient,
    RamistatCoreClient,
)
from config import Config
from middleware import LoggingMiddleware

log = structlog.get_logger()
api_key = environ["API_KEY"]


class WarpResource:
    def on_put(self, req, resp):
        """Handles PUT request to warp positions"""
        rid = req.get_header("X-Request-ID")

        # Cannot warp if the Ontarian Manifold is not at 40000KPGs
        ontarian_manifold = RamistatCoreClient(api_key, rid).diagnostic().text
        if int(ontarian_manifold) != 40000:
            raise falcon.HTTPInternalServerError(
                description="System configuration invalid"
            )

        location = req.get_media()["location"]
        warp = FiromactalDriveClient(api_key, rid).warp(location)

        resp.status = warp.status_code
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = "Engage!" if int(resp.status) == 200 else "Failed!"


class CoolResource:
    def on_put(self, req, resp):
        """Handles PUT request to warp positions"""
        rid = req.get_header("X-Request-ID")

        cool = RamistatCoreClient(api_key, rid).cool()

        resp.status = cool.status_code
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = "Cooled!" if int(resp.status) == 200 else "Failed!"


class DiagnosticResource:
    def on_get(self, req, resp):
        """Handles GET request for full system diagnostics"""
        rid = req.get_header("X-Request-ID")

        location = FiromactalDriveClient(api_key, rid).diagnostic()
        ontarian_manifold = RamistatCoreClient(api_key, rid).diagnostic()

        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = f"{location.text} - {ontarian_manifold.text} KPGs"


class HealthCheckResource:
    def on_get(self, req, resp):
        rid = req.get_header("X-Request-ID")
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = rid


if __name__ == '__main__':
    log.info("Booting up the Isopalavial Interface")

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
    app.add_route("/cool", CoolResource())
    app.add_route("/diagnostic", DiagnosticResource())
    app.add_route("/healthcheck", HealthCheckResource())

    port = Config.IsopalavialInterface.port
    with make_server('', port, app) as httpd:
        print(f"Serving until killed on port {port}...")
        httpd.serve_forever()
