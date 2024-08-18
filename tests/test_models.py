# tests/test_models.py

import pytest
from app import create_app, db
from app.models import Job

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_job_model(app):
    with app.app_context():
        job = Job(
            title='Software Engineer',
            description='Develop and maintain software applications.',
            company_name='Tech Corp',
            location='San Francisco',
            posted_date='2024-08-18'
        )
        db.session.add(job)
        db.session.commit()
        
        assert job.id is not None
        assert job.title == 'Software Engineer'
        assert job.company_name == 'Tech Corp'
