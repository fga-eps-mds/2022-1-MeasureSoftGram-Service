from service.tests import TestCaseExpanded


class SupportedEntitiesEndointTestCase(
    TestCaseExpanded,
):
    def validate_entity_data(self, data):
        """
        Função auxiliar para validar se os dados de uma
        entidade estão respeitando o formato esperado.
        """
        for key in data.keys():
            self.assertIsInstance(key, str)

        keys = set(data.keys())
        expected_keys = {"id", "key", "name", "description"}

        self.assertEqual(keys, expected_keys)
        self.assertIsInstance(data["id"], int)

        self.validate_key(data["key"])

    def validate_supported_entity_datatype(self, url):
        """
        Função genérica que valida se os endpoints de
        supported entities estão retornando dados válidos.
        """
        next_url = url

        while next_url:
            response = self.client.get(path=next_url)
            data = response.json()

            next_url = data["next"]
            data = data["results"]

            for entity_data in data:
                self.validate_entity_data(entity_data)

    def test_if_supported_metrics_endpoint_is_returning_valid_data(self):
        self.validate_supported_entity_datatype(
            url="/api/v1/supported-metrics/",
        )

    def test_if_supported_measures_endpoint_is_returning_valid_data(self):
        self.validate_supported_entity_datatype(
            url="/api/v1/supported-measures/",
        )

    def test_if_supported_subcharacteristics_endpoint_is_returning_valid_data(
        self,
    ):
        self.validate_supported_entity_datatype(
            url="/api/v1/supported-subcharacteristics/",
        )

    def test_if_supported_characteristics_endpoint_is_returning_valid_data(
        self,
    ):
        self.validate_supported_entity_datatype(
            url="/api/v1/supported-characteristics/",
        )
