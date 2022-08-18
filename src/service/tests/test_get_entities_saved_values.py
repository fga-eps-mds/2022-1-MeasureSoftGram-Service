from service.tests import TestCaseExpanded


class EntitiesSavedValuesTestCase(TestCaseExpanded):

    def validate_entity_data(self, data):
        """
        Função auxiliar para validar se os dados de uma
        entidade estão respeitando o formato esperado.
        """
        for key in data.keys():
            self.assertIsInstance(key, str)

        keys = set(data.keys())
        expected_keys = {
            "id", "key", "name",
            "description", "latest",
        }
        self.assertEqual(
            keys,
            expected_keys,
            msg=(
                "As chaves esperadas não foram encontradas. "
                f"Chaves encontradas: {keys}."
                f"Chaves esperadas: {expected_keys}."
            )
        )
        self.assertIsInstance(data["id"], int, msg="O id não é um inteiro.")
        self.validate_key(data["key"])

    def test_if_repository_metrics_endpoint_is_returning_valid_data(self):
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
