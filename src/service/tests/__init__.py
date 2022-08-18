from django.test import TestCase
from django.core.management import call_command


class TestCaseExpanded(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        call_command("load_initial_data")

    def validate_key(self, key):
        """
        Função auxiliar para validar se a key das
        entidades seguem o padrão de nomeação definido.
        """

        for c in key:
            self.assertTrue(
                c.islower() or  c.isalnum() or c == '_',
                msg=(
                    "All characters in key must be lowercase and "
                    f"alphanumeric. The key is {key} and the "
                    f"failed char is {c}"
                ),
            )
