from service.tests import TestCaseExpanded


class TestCreateMetricsTestCase(TestCaseExpanded):
    def test_if_create_metric_endpoint_is_saving_new_values(self):
        url="/api/v1/organizations/1/repository/1/create/metrics/"
        data = {"metric_id": 78, "value": 14}
        response = self.client.post(path=url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = response.json()
        id = data["metric_id"]
        url= f"/api/v1/organizations/1/repository/1/metrics/{id}/" 
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["latest"]["value"], 14)

                                    

