import unittest
from ai_helpers import get_response

class TestAIHelpers(unittest.TestCase):

    def test_response(self):
        self.assertIn("AI Response", get_response("Hello"))

if __name__ == "__main__":
    unittest.main()