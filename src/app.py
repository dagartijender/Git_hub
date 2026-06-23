import json
import logging
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .calculator import add, divide

LOGGER = logging.getLogger(__name__)


def route_request(path: str) -> tuple[HTTPStatus, dict[str, object]]:
    request = urlparse(path)

    if request.path in {"/health", "/ready"}:
        return HTTPStatus.OK, {"status": "ok"}

    if request.path == "/":
        return HTTPStatus.OK, {
            "service": "gitops-calculator",
            "version": os.getenv("APP_VERSION", "development"),
            "endpoints": ["/health", "/ready", "/api/calculate"],
        }

    if request.path != "/api/calculate":
        return HTTPStatus.NOT_FOUND, {"error": "not found"}

    query = parse_qs(request.query)
    try:
        operation = query.get("operation", ["add"])[0]
        left = float(query["left"][0])
        right = float(query["right"][0])

        if operation == "add":
            result = add(left, right)
        elif operation == "divide":
            result = divide(left, right)
        else:
            raise ValueError("operation must be 'add' or 'divide'")
    except (KeyError, ValueError) as error:
        return HTTPStatus.BAD_REQUEST, {"error": str(error)}

    return HTTPStatus.OK, {
        "operation": operation,
        "left": left,
        "right": right,
        "result": result,
    }


class ApiHandler(BaseHTTPRequestHandler):
    server_version = "GitOpsDemo/1.0"

    def do_GET(self) -> None:
        status, payload = route_request(self.path)
        self._send_json(status, payload)

    def log_message(self, format: str, *args: object) -> None:
        LOGGER.info("%s - %s", self.address_string(), format % args)

    def _send_json(self, status: HTTPStatus, payload: dict[str, object]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def create_server(host: str = "0.0.0.0", port: int = 8080) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), ApiHandler)


def main() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(message)s",
    )
    port = int(os.getenv("PORT", "8080"))
    server = create_server(port=port)
    LOGGER.info("gitops-calculator listening on port %s", port)
    server.serve_forever()


if __name__ == "__main__":
    main()
