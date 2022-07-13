from django.contrib.auth import get_user_model
from django.db import models
from simple_history.models import HistoricalRecords

User = get_user_model()


class Organization(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    members = models.ManyToManyField(
        User,
        related_name='organizations',
    )

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)

    github_url = models.URLField(max_length=512)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    organization = models.ForeignKey(
        Organization,
        related_name='projects',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class QualityCaracteristic(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)

    def __str__(self):
        return self.name


class SubQualityCaracteristic(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)

    quality_caracteristic = models.ForeignKey(
        QualityCaracteristic,
        related_name='sub_quality_caracteristics',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Metric(models.Model):
    name = models.CharField(max_length=128)

    subquality_caracteristic = models.ForeignKey(
        SubQualityCaracteristic,
        related_name='metrics',
        on_delete=models.CASCADE,
    )


class Measurement(models.Model):
    name = models.CharField(max_length=128)
    value = models.FloatField()

    project = models.ForeignKey(
        Project,
        related_name='measurements',
        on_delete=models.DO_NOTHING,
    )


# class DataInput(models.Model):
#     """
#     Tabela que salva todos os dados de inputs
#     recebidos durante a coleta de métricas
#     """

#     data = models.JSONField()
#     project = models.ForeignKey(Project, related_name='data_inputs')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


class PreConfig(models.Model):
    """
    Model que representa as configurações de um modelo de qualidade.
    No nosso léxico essa modelo é chamada de pré-configuração
    """
    project = models.ForeignKey(
        Project,
        related_name='configurations',
        on_delete=models.DO_NOTHING,
    )
    setting = models.JSONField()
    history = HistoricalRecords()

    num = models.IntegerField(default=0)

    def __str__(self):
        return self.name