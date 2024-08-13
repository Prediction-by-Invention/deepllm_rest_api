import unittest

from fastapi.testclient import TestClient

from src.server.main import app

client = TestClient(app)


class TestApp(unittest.TestCase):
    client = TestClient(app)

    def test_root(self):
        response = client.get("/")
        self.assertTrue(response.status_code == 200)


if __name__ == "__main__":
    unittest.main()
