import pytest
import logging
from django.urls import reverse
from django.conf import settings

@pytest.mark.django_db
def test_logging_configuration():
    # Verify the LOGGING dictionary exists and has correct loggers
    assert 'LOGGING' in dir(settings)
    assert 'cloudstudent' in settings.LOGGING['loggers']
    assert 'django.request' in settings.LOGGING['loggers']

@pytest.mark.django_db
def test_request_id_in_response(client):
    resp = client.get(reverse('accounts:login'))
    assert resp.status_code == 200
    assert 'X-Request-ID' in resp.headers
    assert len(resp.headers['X-Request-ID']) > 10

@pytest.mark.django_db
def test_health_endpoint(client):
    resp = client.get(reverse('health'))
    assert resp.status_code == 200
    assert resp.json()['status'] == 'ok'
    assert resp.json()['database'] == 'connected'

@pytest.mark.django_db
def test_authentication_logging(client, caplog):
    caplog.set_level(logging.INFO, logger='cloudstudent.security')
    
    # Test failed login
    resp = client.post(reverse('accounts:login'), {'username': 'wrong', 'password': 'wrong'})
    assert resp.status_code == 200
    
    # Check if failed login attempt was logged
    found_warning = False
    for record in caplog.records:
        if record.levelname == 'WARNING' and 'Failed login attempt' in record.message and 'wrong' in record.message:
            found_warning = True
            break
    assert found_warning

@pytest.mark.django_db
def test_successful_authentication_logging(client, custom_admin_user, caplog):
    caplog.set_level(logging.INFO, logger='cloudstudent.security')
    
    client.post(reverse('accounts:login'), {'username': 'admin_test_cf', 'password': 'test-only-password'})
    
    found_info = False
    for record in caplog.records:
        if record.levelname == 'INFO' and 'Successful login' in record.message and 'admin_test_cf' in record.message:
            found_info = True
            break
    assert found_info

@pytest.mark.django_db
def test_request_logging_middleware(client, caplog):
    caplog.set_level(logging.INFO, logger='cloudstudent.request')
    client.get(reverse('accounts:login'))
    
    found = False
    for record in caplog.records:
        if record.levelname == 'INFO' and 'method=GET' in record.message and 'status=200' in record.message:
            found = True
            break
    assert found
