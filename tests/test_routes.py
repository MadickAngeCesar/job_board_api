import pytest
from app import create_app, db

@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app.test_client()

def test_submit_job_application(test_client):
    data = {
        'user_id': 1,
        'job_id': 1,
        'resume': (open('test_resume.pdf', 'rb'), 'test_resume.pdf'),
        'cover_letter': (open('test_cover_letter.pdf', 'rb'), 'test_cover_letter.pdf')
    }
    response = test_client.post('/api/job/apply', data=data)
    assert response.status_code == 201

def test_get_application_status(test_client):
    response = test_client.get('/api/application/status?user_id=1&job_id=1')
    assert response.status_code == 200
    assert response.json['status'] == 'submitted'
