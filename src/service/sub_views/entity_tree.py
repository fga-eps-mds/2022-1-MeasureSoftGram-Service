"""
Módulo que agrupa as views relacionadas à árvore de entidades. Quando dizemos
árvore de entidades, estamos falando do relacionamentos entre as entidades.
Isso é:
* Características com subcaracterísticas
* Subcaracterísticas com medidas
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response

from service import models, serializers


@api_view(['GET', 'HEAD', 'OPTIONS'])
def entity_relationship_tree(request):
    """
    Retorna a árvore de relacionamentos entre as entidades
    """
    qs = models.SupportedCharacteristic.objects.all().prefetch_related(
        'subcharacteristics', 'subcharacteristics__measures',
    )

    serializer = serializers.CharacteristicEntityRelationshipTreeSerializer(
        qs,
        many=True,
    )

    return Response(serializer.data)
