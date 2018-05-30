from hashlib import sha1
import hmac
import json
from flask import url_for


def test_post_not_found(client):
    response = client.post('does_not_exist')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 404
    assert 'Not found.' in data['message']


def test_post_no_repo(client, secret):
    req_data = json.dumps({
        'ref': 'test_branch',
        'repository': {'full_name': 'does_not_exist'}
    })
    signature = hmac.new(secret, req_data.encode('utf-8'), sha1).hexdigest()
    headers = {'X-Hub-Signature': 'sha1=' + signature,
               'X-Github-Event': 'test_event'}
    response = client.post(url_for('build'), data=req_data,
                           headers=headers, content_type='application/json')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 404
    assert 'Not found.' in data['message']


def test_post_no_event(client, request_json, signature):
    headers = {'X-Hub-Signature': 'sha1=' + signature,
               'X-Github-Event': 'does_not_exist'}
    response = client.post(url_for('build'), data=request_json,
                           headers=headers, content_type='application/json')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 404
    assert 'Not found.' in data['message']


def test_post_no_ref(client, secret):
    req_data = json.dumps({
        'ref': 'does_not_exist',
        'repository': {'full_name': 'test_consumer'}
    })
    signature = hmac.new(secret, req_data.encode('utf-8'), sha1).hexdigest()
    headers = {'X-Hub-Signature': 'sha1=' + signature,
               'X-Github-Event': 'test_event'}
    response = client.post(url_for('build'), data=req_data,
                           headers=headers, content_type='application/json')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 404
    assert 'Not found.' in data['message']
