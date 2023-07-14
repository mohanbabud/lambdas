import unittest
from unittest.mock import patch
import stormcontrol  # Import your lambda function code


class TestLambdaFunction(unittest.TestCase):

    def test_getAlarms_with_matching_filter(self):
        event = {
            "Records": [
                {
                    "EventSource": "aws:sns",
                    "Sns": {
                        "Message": "{\"Message\":{\"Severity\":\"high\",\"ARN\":\"Dummy\",\"Account\":\"TestAccount\",\"summary\": \"Matchme\"}}"
                    }
                }
            ]
        }
        stats = {
            "received": 0,
            "queued": 0,
            "suppressed": 0
        }
        filters = {
            "summary": "Matchme"
        }

        with patch('stormcontrol.json.loads') as mock_json_loads:
            # Mocking json.loads to return the original message for testing
            mock_json_loads.return_value = event['Records'][0]['Sns']['Message']

            # Call the lambda_handler function from your code
            stormcontrol.lambda_handler(event, None)

            # Assert the expected values
            self.assertEqual(stats['received'], 1)
            self.assertEqual(stats['queued'], 0)
            self.assertEqual(stats['suppressed'], 1)

    # Add more test cases as needed


if __name__ == '__main__':
    unittest.main()
