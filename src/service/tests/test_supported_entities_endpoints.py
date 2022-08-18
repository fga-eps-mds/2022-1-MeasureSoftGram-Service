from django.test import TestCase
from django.core.management import call_command


class SupportedEntitiesEndointTestCase(TestCase):
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
        expected_keys = {"id", "key", "name", "description"}
        self.assertEqual(keys, expected_keys)

        self.assertIsInstance(data["id"], int)
        key = data["key"]
        self.validate_key(key)

    def validate_supported_entity_datatype(self, url):
        next_url = url

        while next_url:
            response = self.client.get(path=next_url)
            data = response.json()

            next_url = data["next"]
            data = data["results"]

            for entity_data in data:
                self.validate_entity_data(entity_data)

    def test_supported_metrics_datatype(self):
        self.validate_supported_entity_datatype(
            url="/api/v1/supported-metrics/",
        )

    def test_supported_measures_datatype(self):
        self.validate_supported_entity_datatype(
            url="/api/v1/supported-measures/",
        )

    def test_supported_subcharacteristics_datatype(self):
        self.validate_supported_entity_datatype(
            url="/api/v1/supported-subcharacteristics/",
        )

    def test_supported_characteristics_datatype(self):
        self.validate_supported_entity_datatype(
            url="/api/v1/supported-characteristics/",
        )

