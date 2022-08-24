from service.tests import TestCaseExpanded


class TestCalculateMeasures(TestCaseExpanded):
    def test_if_calculate_measures_endpoint_is_working(self):
        url="/api/v1/organizations/1/repository/1/calculate/measures/"
        data = {"measures": [{ "key": "passed_tests" }]}
        response = self.client.post(path=url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = response.json()
        value = data["lastest"]["value"]
        id = data["id"]
        url= f"/api/v1/organizations/1/repository/1/measures/{id}/" 
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["latest"]["value"], value)

