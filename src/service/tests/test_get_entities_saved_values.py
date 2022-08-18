from django.test import TestCase
from django.core.management import call_command



class EntitiesSavedValuesTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        call_command("load_initial_data")

    def validate_key(self, key):
        for c in key:
            self.assertTrue(
                c.islower() or  c.isalnum() or c == '_',
                msg=(
                    "All characters in key must be lowercase and "
                    f"alphanumeric. The key is {key} and the "
                    f"failed char is {c}"
                ),
            )

    def validate_entity_data(self, data):
        for key in data.keys():
            self.assertIsInstance(key, str)

        keys = set(data.keys())
        expected_keys = {
            "id", "key", "name",
            "description", "latest",
        }
        self.assertEqual(keys, expected_keys)

        self.assertIsInstance(data["id"], int)
        key = data["key"]
        self.validate_key(key)

    def test_metrics_saved_values(self):
        next_url = (
            "/api/v1/organizations/1/"
            "repository/1/metrics/"
        )

        while next_url:
            response = self.client.get(path=next_url)
            data = response.json()

            next_url = data["next"]
            data = data["results"]

            for entity_data in data:
                self.validate_entity_data(entity_data)

