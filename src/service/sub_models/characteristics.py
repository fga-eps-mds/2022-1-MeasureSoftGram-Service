from typing import Iterable, Set

from django.db import models

import utils


class SupportedCharacteristic(models.Model):
    """
    Classe que abstrai uma característica suportada pelo sistema.
    """
    name = models.CharField(max_length=128)
    key = models.CharField(max_length=128, unique=True)
    description = models.TextField(
        max_length=512,
        null=True,
        blank=True,
    )
    subcharacteristics = models.ManyToManyField(
        'SupportedSubCharacteristic',
        related_name='related_characteristics',
        blank=True,
    )

    def has_unsupported_subcharacteristics(
        self,
        subcharacteristics_keys: Iterable[str],
    ) -> Set[str]:
        """
        Verifica se todas as subcaracterísticas passadas no argumento
        `subcharacteristics_keys` estão associadas a característica no modelo.

        Retorna um set com as subcaracterísticas que não estão associadas
        a característica.
        """
        subcharacteristics_keys = set(subcharacteristics_keys)

        qs = self.subcharacteristics.all()
        related_subcharacteristics: Set[str] = set(
            qs.values_list('key', flat=True)
        )

        return subcharacteristics_keys - related_subcharacteristics

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para validar se o campo `key` é valido
        """
        if not self.key and self.name:
            self.key = utils.namefy(self.name)

        elif not self.name and self.key:
            self.name = utils.keyfy(self.key)

        super().save(*args, **kwargs)

    @staticmethod
    def has_unsupported_characteristics(
        selected_characteristics_keys: Iterable[str]
    ) -> Set[str]:
        """
        Verifica se existe alguma característica não suportada, e caso exista
        é retornado a lista das keys das características não suportadas.
        """
        return utils.has_unsupported_entity(
            selected_characteristics_keys,
            SupportedCharacteristic,
        )