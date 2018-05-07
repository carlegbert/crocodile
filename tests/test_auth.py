from flask import url_for
from hashlib import sha1
import hmac
import json


def test_put_no_signature(client):
    response = client.post(url_for('build'))
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 401
    assert 'Authorization denied' in data['message']


def test_put_bad_signature(client):
    req_data = json.dumps({'dict': 'with some stuff'})
    secret = 'bad_secret'.encode('utf-8')
    signature = hmac.new(secret, req_data.encode('utf-8'), sha1).hexdigest()
    headers = {'X-Hub-Signature': 'sha1=' + signature}
    response = client.post(url_for('build'), data=req_data, headers=headers,
                           content_type='application/json')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 401
    assert 'Authorization denied' in data['message']


def test_put_good_signature(client):
    req_data = json.dumps({'ref': 'test_branch'})
    secret = 'test_secret'.encode('utf-8')
    signature = hmac.new(secret, req_data.encode('utf-8'), sha1).hexdigest()
    headers = {'X-Hub-Signature': 'sha1=' + signature,
               'X-Github-Event': 'test_event'}
    response = client.post(url_for('build'), data=req_data, headers=headers,
                           content_type='application/json')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 202
    assert 'Hook consumed' in data['message']
