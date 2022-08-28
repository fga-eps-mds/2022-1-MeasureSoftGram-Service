from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

from organizations.models import Organization, Product, Repository
from organizations.serializers import (
    OrganizationSerializer,
    ProductSerializer,
    RepositoriesSQCHistorySerializer,
    RepositorySerializer,
    RepositorySQCLatestValueSerializer,
)


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    Endpoint das organizações

    * `GET`: Lista todas as organizações
    * `POST`: Cria uma nova organização
    * `PUT` ou `PATCH`: Atualiza uma organização
    * `DELETE`: Deleta uma organização
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_organization(self):
        return get_object_or_404(
            Organization,
            id=self.kwargs['organization_pk'],
        )

    def get_queryset(self):
        organization = self.get_organization()
        return Product.objects.filter(organization=organization)

    def perform_create(self, serializer):
        organization = self.get_organization()
        serializer.save(organization=organization)


class RepositoryViewSet(viewsets.ModelViewSet):
    serializer_class = RepositorySerializer
    queryset = Repository.objects.all()

    def perform_create(self, serializer):
        product = get_object_or_404(
            Product,
            id=self.kwargs['product_pk'],
        )
        serializer.save(product=product)

    def get_queryset(self):
        product = get_object_or_404(Product, id=self.kwargs['product_pk'])
        return Repository.objects.filter(product=product)


class RepositoriesSQCLatestValueViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Lista o SQC mais recente dos repositórios de um produto
    """
    serializer_class = RepositorySQCLatestValueSerializer

    def get_queryset(self):
        product = get_object_or_404(Product, id=self.kwargs['product_pk'])
        qs = Repository.objects.filter(product=product)
        qs = qs.prefetch_related(
            'calculated_sqcs',
            'product',
            'product__organization',
        )
        return qs


class RepositoriesSQCHistoryViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = RepositoriesSQCHistorySerializer

    def get_queryset(self):
        product = get_object_or_404(Product, id=self.kwargs['product_pk'])
        qs = Repository.objects.filter(product=product)
        qs = qs.prefetch_related(
            'calculated_sqcs',
            'product',
            'product__organization',
        )
        return qs