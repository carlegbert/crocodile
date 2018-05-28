from hashlib import sha1
import hmac
from flask import url_for
import json


def test_post_no_signature(client):
    response = client.post(url_for('build'))
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 401
    assert 'Authorization denied' in data['message']


def test_post_bad_signature(client):
    req_data = json.dumps({'dict': 'with some stuff'})
    secret = 'bad_secret'.encode('utf-8')
    signature = hmac.new(secret, req_data.encode('utf-8'), sha1).hexdigest()
    headers = {'X-Hub-Signature': 'sha1=' + signature}
    response = client.post(url_for('build'), data=req_data,
                           headers=headers, content_type='application/json')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 401
    assert 'Authorization denied' in data['message']


def test_post_good_signature(client, secret, request_json, headers):
    response = client.post(url_for('build'), data=request_json,
                           headers=headers, content_type='application/json')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 202
    assert 'Hook consumed' in data['message']


def test_invalid_ip_rejected(client, request_json, headers):
    client.environ_base['REMOTE_ADDR'] = '123.4.5.6'
    response = client.post(url_for('build'), data=request_json,
                           headers=headers, content_type='application/json')
    client.environ_base['REMOTE_ADDR'] = '127.0.0.1'
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 401
    assert 'Authorization denied' in data['message']
