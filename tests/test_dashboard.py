from flask import url_for


def test_get_index(client):
    response = client.get(url_for('dashboard'))
    assert response.status_code == 200
