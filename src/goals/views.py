from rest_framework import mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse

from goals.models import Goal
from goals.serializers import GoalSerializer
from organizations.models import Product


class CurrentGoalModelViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

    def this_product_does_not_have_a_goal_reponse(self, product):
        create_a_new_goal_url = reverse(
            'create-goal-list',
            kwargs={
                "product_pk": product.id,
                "organization_pk": product.organization.id,
            },
            request=self.request,
        )

        data = {
            'detail': 'This product does not have a goal.',
            'actions': {
                'create a new goal': create_a_new_goal_url,
            }
        }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        # first() == mais recente == goal atual
        product = get_object_or_404(
            Product,
            pk=kwargs["product_pk"],
            organization_id=kwargs["organization_pk"],
        )
        latest_goal = Goal.objects.filter(product=product).first()

        if not latest_goal:
            return self.this_product_does_not_have_a_goal_reponse(product)

        serializer = GoalSerializer(latest_goal)
        return Response(serializer.data, status.HTTP_200_OK)


class CreateGoalModelViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()

    def get_product(self):
        return get_object_or_404(
            Product,
            id=self.kwargs['product_pk'],
            organization_id=self.kwargs['organization_pk'],
        )

    def perform_create(self, serializer):
        product = self.get_product()
        serializer.save(product=product)
