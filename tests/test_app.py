import unittest
from http import HTTPStatus

from src.app import route_request


class ApiTests(unittest.TestCase):
    def test_health_endpoint(self):
        status, body = route_request("/health")
        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(body, {"status": "ok"})

    def test_add_endpoint(self):
        status, body = route_request(
            "/api/calculate?operation=add&left=2&right=3"
        )
        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(body["result"], 5)

    def test_divide_endpoint(self):
        status, body = route_request(
            "/api/calculate?operation=divide&left=10&right=2"
        )
        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(body["result"], 5)

    def test_invalid_operation_returns_bad_request(self):
        status, body = route_request(
            "/api/calculate?operation=multiply&left=2&right=3"
        )
        self.assertEqual(status, HTTPStatus.BAD_REQUEST)
        self.assertIn("operation must be", body["error"])

    def test_missing_operand_returns_bad_request(self):
        status, _ = route_request("/api/calculate?operation=add&left=2")
        self.assertEqual(status, HTTPStatus.BAD_REQUEST)

    def test_unknown_endpoint_returns_not_found(self):
        status, body = route_request("/missing")
        self.assertEqual(status, HTTPStatus.NOT_FOUND)
        self.assertEqual(body, {"error": "not found"})


if __name__ == "__main__":
    unittest.main()
