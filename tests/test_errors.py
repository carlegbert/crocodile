from flask import url_for
import json


def test_get_not_found(client):
    response = client.get('does_not_exist')
    expected_response = 'The page you are trying to visit does not exist.'
    assert response.status_code == 404
    assert expected_response in str(response.data)


def test_put_not_found(client):
    response = client.post('does_not_exist')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 404
    assert 'Not found.' in data['message']


def test_put_no_digest(client):
    response = client.post(url_for('build'))
    assert response.status_code == 401
    data = json.loads(response.data.decode('utf-8'))
    assert 'Authorization denied' in data['message']
