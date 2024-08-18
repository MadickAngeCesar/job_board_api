# tests/test_routes.py

import pytest
from app import create_app, db
from app.models import Job

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_job(client):
    response = client.post('/api/job/apply', data={
        'title': 'Software Engineer',
        'description': 'Develop and maintain software applications.',
        'company_name': 'Tech Corp',
        'location': 'San Francisco',
        'resume': (open('tests/test_resume.pdf', 'rb'), 'test_resume.pdf'),
        'cover_letter': (open('tests/test_cover_letter.pdf', 'rb'), 'test_cover_letter.pdf')
    })
    assert response.status_code == 201
    assert b'Application submitted successfully' in response.data

def test_get_application_status(client):
    # Assuming you have a job with ID 1 in your test database
    response = client.get('/api/application/status', query_string={'application_id': 1})
    assert response.status_code == 200
    assert b'Application Status:' in response.data
