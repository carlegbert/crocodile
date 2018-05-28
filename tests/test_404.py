import json


def test_post_not_found(client):
    response = client.post('does_not_exist')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 404
    assert 'Not found.' in data['message']
