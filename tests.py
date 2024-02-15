import pytest
from flask_testing import TestCase
from app import app, driver
from neo4j.exceptions import ClientError

class MyTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        with driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def tearDown(self):
        with driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def test_create_node(self):
        response = self.client.post('/nodes', json={
            "document": "test document",
            "keywords": ["test1", "test2"],
            "source": "test source",
            "credibility": 0.8,
            "accuracy": 0.9,
            "authenticity": 0.7,
            "confidence": 0.6,
            "relevance": 0.5,
            "type": "test type"
        })
        assert response.status_code == 201
        assert 'id' in response.json

    def test_get_node_not_found(self):
        response = self.client.get('/nodes/1')
        assert response.status_code == 404
        assert response.json == {'error': 'Node not found'}

    # todo: add more tests

if __name__ == '__main__':
    pytest.main()