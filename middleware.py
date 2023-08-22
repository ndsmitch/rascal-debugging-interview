from time import time
from uuid import uuid4

import json
import structlog


class LoggingMiddleware:
    def __init__(self, log):
        self.log = log

    def process_request(self, req, resp):
        # Assume a network proxy adds incoming request IDs
        # throws 400 BadRequest if missing
        rid=req.get_header("X-Request-ID", required=True)

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            time=time(),
            method=req.method,
            uri=req.relative_uri,
            rid=rid,
        )
        self.log.bind()

    def process_response(self, req, resp, resource, req_succeeded):
        rid=req.get_header("X-Request-ID", required=True)
        resp.set_header('X-Request-ID', rid)

        log = {
            "reqHeaders": req.headers,
            "reqMedia": req.media,
            "status": resp.status,
        }

        if req_succeeded:
            self.log.info(json.dumps(log, ensure_ascii=False))
        else:
            self.log.error(json.dumps(log, ensure_ascii=False))

