import unittest
from fastapi.testclient import TestClient
from backend.app import app

class TestAPIIntegration(unittest.TestCase):
    """
    Automated API Integration Suite for RealityCheck AI.
    Runs HTTP mock queries to test routes, status codes, and error exceptions.
    """

    @classmethod
    def setUpClass(cls):
        # Initialize the FastAPI TestClient
        cls.client = TestClient(app)

    def test_health_check_endpoint(self):
        """
        Ensures GET /health loads healthy configuration descriptors.
        """
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data["status"], "online")
        self.assertEqual(json_data["service"], "RealityCheck AI – Fake News & Misinformation Analyzer")
        self.assertIn("capabilities", json_data)

    def test_analyze_pure_text_success(self):
        """
        Ensures POST /analyze processes valid text payloads and satisfies JSON contracts.
        """
        payload = {
            "text": "The international space agency released satellite pictures detailing atmospheric ice cloud changes."
        }
        response = self.client.post("/analyze", json=payload)
        self.assertEqual(response.status_code, 200)
        
        body = response.json()
        self.assertEqual(body["status"], "success")
        
        data = body["data"]
        self.assertEqual(data["input_type"], "text")
        self.assertEqual(data["source"], "Direct Text Input")
        self.assertIn("score", data)
        self.assertIn("fake_probability", data)
        self.assertIn("bias", data)
        self.assertIn("highlights", data)
        self.assertIn("explanations", data)
        self.assertIn("raw_text", data)
        
        # Verify typing matches Pydantic declarations
        self.assertIsInstance(data["score"], int)
        self.assertIsInstance(data["fake_probability"], float)
        self.assertIsInstance(data["bias"], str)
        self.assertIsInstance(data["highlights"], list)

    def test_analyze_url_success(self):
        """
        Ensures POST /analyze resolves URL payloads and handles Reputation registers.
        """
        payload = {
            "url": "https://www.bbc.com/news/world-654321"
        }
        response = self.client.post("/analyze", json=payload)
        self.assertEqual(response.status_code, 200)
        
        body = response.json()
        data = body["data"]
        self.assertEqual(data["input_type"], "url")
        self.assertEqual(data["source"], "bbc.com")
        self.assertIn("score", data)

    def test_analyze_empty_payload_rejection(self):
        """
        Ensures empty payload triggers Bad Request (400) validations with clear warnings.
        """
        payload = {}
        response = self.client.post("/analyze", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.json())

    def test_analyze_empty_fields_rejection(self):
        """
        Ensures blank text blocks fail validation checks with appropriate error logs.
        """
        payload = {
            "text": "    "
        }
        response = self.client.post("/analyze", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("empty", response.json()["detail"].lower())

    def test_analyze_invalid_url_rejection(self):
        """
        Ensures non-HTTP URL payloads throw descriptive validation errors.
        """
        payload = {
            "url": "invalid-url-string"
        }
        response = self.client.post("/analyze", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("url", response.json()["detail"].lower())

if __name__ == "__main__":
    unittest.main()
