from typing import Dict

from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token

from organizations.models import Organization, Product

from utils.tests import APITestCaseExpanded

User = get_user_model()


class ProductsViewsSetCase(APITestCaseExpanded):

    def test_create_a_new_product(self):
        org = self.get_organization()
        url = reverse("product-list", args=[org.id])
        data = {
            "name": "Test Product",
            "description": "Test Product Description",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

        data = response.json()

        self.assertEqual(data["name"], "Test Product")
        self.assertEqual(data["description"], "Test Product Description")

        qs = Product.objects.filter(name="Test Product")

        self.assertEqual(qs.exists(), True)
        self.assertEqual(qs.count(), 1)

        product = qs.first()

        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.description, "Test Product Description")

        self.assertEqual(product.organization, org)

    def compare_product_data(self, data, product):
        self.assertEqual(data["id"], product.id)
        self.assertEqual(data["name"], product.name)
        self.assertEqual(data["description"], product.description)

    def test_if_existing_product_is_being_listed(self):
        org = self.get_organization()
        product = self.get_product(org)

        url = reverse("product-list", args=[org.id])
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]
        self.compare_product_data(data[0], product)

    def test_if_only_organization_products_is_being_listed(self):
        org1 = self.get_organization(name="Organization 1")
        org2 = self.get_organization(name="Organization 2")

        self.get_product(org1, name="Test Product 1")
        self.get_product(org1, name="Test Product 2")

        self.get_product(org2, name="Test Product 3")

        url = reverse("product-list", args=[org2.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data['count'], 1)
        self.assertEqual(len(data['results']), data['count'])
        product = data['results'][0]

        self.assertEqual(product['name'], "Test Product 3")

    def test_update_a_existing_product(self):
        org = self.get_organization()
        product = self.get_product(org)
        url = reverse("product-detail", args=[org.id, product.id])
        data = {
            "name": "Test Product Updated",
            "description": "Test Product Description Updated",
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, 200)
        data = response.json()

        product = Product.objects.get(id=product.id)
        self.compare_product_data(data, product)

    def test_patch_update_a_existing_product(self):
        org = self.get_organization()
        product = self.get_product(org)
        url = reverse("product-detail", args=[org.id, product.id])
        data = {
            "name": "Test Product Updated",
            "description": "Test Product Description Updated",
        }
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, 200)
        data = response.json()

        product = Product.objects.get(id=product.id)
        self.compare_product_data(data, product)

    def test_delete_a_existing_product(self):
        org = self.get_organization()
        product = self.get_product(org)
        url = reverse("product-detail", args=[org.id, product.id])
        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, 204)
        qs = Product.objects.filter(id=product.id).exists()
        self.assertEqual(qs, False)

        url = reverse("product-detail", args=[org.id, product.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 404)

        url = reverse("product-list", args=[org.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data['count'], 0)

    def test_if_existing_products_is_being_listed(self):
        org = self.get_organization()

        self.get_product(org, name="Test Product 1")
        self.get_product(org, name="Test Product 2")
        self.get_product(org, name="Test Product 3")

        url = reverse("product-list", args=[org.id])
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data['count'], 3)
        self.assertEqual(len(data['results']), data['count'])

        self.assertEqual(data['next'], None)
        self.assertEqual(data['previous'], None)
        self.assertEqual(data['results'][2]['name'], "Test Product 1")
        self.assertEqual(data['results'][1]['name'], "Test Product 2")
        self.assertEqual(data['results'][0]['name'], "Test Product 3")

    def test_if_product_attribute_key_is_being_set(self):
        """
        Testa se o atributo key está sendo setado corretamente
        "produto do dagrão!" -> "produto-do-dagrao"
        """
        org = self.get_organization()
        product = self.get_product(
            org,
            name="produto do dagrão!",
        )
        url = reverse("product-detail", args=[org.id, product.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)

        key = response.json()["key"]

        self.assertEqual(key, "test-organization-produto-do-dagrao")
        self.assertEqual(product.key, "test-organization-produto-do-dagrao")

    def test_if_an_product_repositories_urls_list_is_returned(self):
        org = self.get_organization()
        product = self.get_product(org)
        self.get_repository(product)

        url = reverse("product-detail", args=[org.id, product.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIsInstance(data["repositories"], list)
        self.assertEqual(len(data["repositories"]), 1)

        url = data["repositories"][0]
        self.assertIsInstance(url, str)

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["name"], "Test Repository")
        self.assertEqual(data["description"], "Test Repository Description")

    def assert_action_in_action_data(
        self,
        action_name,
        action_data,
    ):
        self.assertIn(
            action_name,
            action_data,
            f"`{action_name}` should be in the actions dictinary",
        )

    def test_if_create_product_action_url_is_working(self):
        org: Organization = self.get_organization()
        product = self.get_product(org)
        url = reverse("product-detail", args=[org.id, product.id])

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIn(
            "actions",
            data,
            "actions key should be in the product data",
        )

        actions = data["actions"]

        expected_actions = [
            "create a new repository",
            "get current goal",
            "get compare all goals",
            "get current pre-config",
            "get pre-config entity relationship tree",
            "get all repositories latest sqcs",
            "get all repositories sqc historical values",
            "create a new goal",
            "create a new pre-config",
        ]

        for action_name in expected_actions:
            self.assert_action_in_action_data(
                action_name,
                actions,
            )

    def get_product_actions(self) -> Dict[str, str]:
        org: Organization = self.get_organization()
        product = self.get_product(org)
        url = reverse("product-detail", args=[org.id, product.id])
        response = self.client.get(url, format="json")
        data = response.json()
        actions = data["actions"]
        return actions, product

    def test_if_get_current_pre_config_url_is_working(self):
        actions, product = self.get_product_actions()
        action_url = actions["get current pre-config"]
        response = self.client.get(action_url)
        self.assertEqual(response.status_code, 200)

    def test_if_create_a_new_repository_action_url_is_working(self):
        actions, product = self.get_product_actions()
        action_url = actions["create a new repository"]
        data = {"name": "Test Repository"}
        response = self.client.post(action_url, data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_if_get_all_repos_sqcs_action_url_is_working(self):
        actions, product = self.get_product_actions()
        action_url = actions["get all repositories latest sqcs"]
        response = self.client.get(action_url)
        self.assertEqual(response.status_code, 200)

    def test_if_get_all_repos_sqcs_history_action_url_is_working(self):
        actions, product = self.get_product_actions()
        action_url = actions["get all repositories sqc historical values"]
        response = self.client.get(action_url)
        self.assertEqual(response.status_code, 200)

    def test_if_create_new_goal_action_url_is_working(self):
        actions, product = self.get_product_actions()
        action_url = actions["create a new goal"]
        data = self.get_goal_data()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.create(
            user=User.objects.create(username='username', email='test_user@email.com')).key
        )

        response = self.client.post(action_url, data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_if_create_new_pre_config_action_url_is_working(self):
        actions, product = self.get_product_actions()
        action_url = actions["create a new pre-config"]
        measures = [{"key": "passed_tests", "weight": 100}]
        subcharacteristics = [{
            "key": "testing_status",
            "weight": 100,
            "measures": measures
        }]
        characteristics = [{
            "key": "reliability",
            "weight": 100,
            "subcharacteristics": subcharacteristics
        }]
        data = {
            "name": "Test Pre-Config",
            "data": {"characteristics": characteristics}
        }
        response = self.client.post(action_url, data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_if_get_current_goal_url_is_working(self):
        actions, product = self.get_product_actions()
        product.goals.create(
            release_name='v1.0',
            created_by=User.objects.create(username='username', email='test_user@email.com'),
            start_at='2020-01-01T00:00:00-03:00',
            end_at='2021-01-01T00:00:00-03:00',
            data={
                'reliability': 53,
                'maintainability': 53,
                'functional_suitability': 53,
            }
        )
        current_goal_url = actions["get current goal"]
        response = self.client.get(current_goal_url)
        self.assertEqual(response.status_code, 200)

    def test_if_get_pre_config_entity_relationship_tree_url_is_working(self):
        actions, product = self.get_product_actions()
        pre_config_entity_relationship_tree_url = actions[
            "get pre-config entity relationship tree"
        ]
        response = self.client.get(pre_config_entity_relationship_tree_url)
        self.assertEqual(response.status_code, 200)

    def test_if_get_all_repositories_latest_sqcs_url_is_working(self):
        actions, product = self.get_product_actions()
        get_all_repositories_latest_sqcs_url = actions[
            "get all repositories latest sqcs"
        ]
        response = self.client.get(get_all_repositories_latest_sqcs_url)
        self.assertEqual(response.status_code, 200)

    def test_if_get_all_repositories_sqc_historical_values_url_is_working(self):
        actions, product = self.get_product_actions()
        get_all_repositories_sqc_historical_values_url = actions[
            "get all repositories sqc historical values"
        ]
        response = self.client.get(get_all_repositories_sqc_historical_values_url)
        self.assertEqual(response.status_code, 200)

    def test_if_is_not_allowed_to_create_products_with_same_name(self):
        org = self.get_organization()
        url = reverse("product-list", args=[org.id])
        data = {
            "name": "Test Product",
            "description": "Test Product Description",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
