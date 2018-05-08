from flask import url_for
import json


def test_method_not_allowed(client):
    response = client.get(url_for('build'))
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 405
    assert 'Method not allowed' in data['message']
