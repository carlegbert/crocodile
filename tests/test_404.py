from hashlib import sha1
import hmac
import json
from flask import url_for


def test_post_not_found(client):
    response = client.post('does_not_exist')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 404
    assert 'Not found.' in data['message']


def test_post_no_customer(client, secret):
    req_data = json.dumps({'ref': 'does_not_exist'})
    signature = hmac.new(secret, req_data.encode('utf-8'), sha1).hexdigest()
    headers = {'X-Hub-Signature': 'sha1=' + signature,
               'X-Github-Event': 'test_event'}
    response = client.post(url_for('build'), data=req_data,
                           headers=headers, content_type='application/json')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 404
    assert 'Not found.' in data['message']
