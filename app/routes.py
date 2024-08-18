from flask import Blueprint, request, jsonify, render_template
from app.models import User, Job, Application
from . import db
from firebase_admin import storage
from datetime import datetime

user_bp = Blueprint('user_bp', __name__)
job_bp = Blueprint('job_bp', __name__)
application_bp = Blueprint('application_bp', __name__)
index_bp = Blueprint('index_bp', __name__)

@index_bp.route('/')
def index():
    return render_template('index.html')

# User registration
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': 'Username already exists'}), 400

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': 'Email already exists'}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# User login (mock login without tokens)
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user is None or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({'message': 'Logged in successfully'}), 200

# Job creation
@job_bp.route('/', methods=['POST'])
def create_job():
    data = request.get_json()
    job = Job(
        title=data['title'],
        description=data['description'],
        company_name=data['company_name'],
        location=data['location'],
        posted_date=data.get('posted_date', datetime.utcnow())  # Provide default value
    )
    db.session.add(job)
    db.session.commit()
    return jsonify(job.to_dict()), 201

# Get all jobs
@job_bp.route('/', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    return jsonify([job.to_dict() for job in jobs]), 200

# Get job by ID
@job_bp.route('/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.query.get_or_404(job_id)
    return jsonify(job.to_dict()), 200

@job_bp.route('/search', methods=['GET'])
def search_jobs():
    title = request.args.get('title')
    if not title:
        return jsonify({'message': 'Job title is required'}), 400

    jobs = Job.query.filter(Job.title.ilike(f'%{title}%')).all()
    result = []
    for job in jobs:
        result.append({
            'id': job.id,
            'title': job.title,
            'description': job.description,
            'company_name': job.company_name,
            'location': job.location,
            'posted_date': job.posted_date
        })
    return jsonify(result), 200


# Application submission
@application_bp.route('/', methods=['POST'])
def submit_application():
    user_id = request.form.get('user_id')
    job_id = request.form.get('job_id')
    resume = request.files['resume']
    cover_letter = request.files['cover_letter']

    # Firebase Storage
    bucket = storage.bucket()
    resume_blob = bucket.blob(f'resumes/{resume.filename}')
    resume_blob.upload_from_file(resume)
    cover_letter_blob = bucket.blob(f'cover_letters/{cover_letter.filename}')
    cover_letter_blob.upload_from_file(cover_letter)

    application = Application(
        user_id=user_id,
        job_id=job_id,
        resume=resume_blob.public_url,
        cover_letter=cover_letter_blob.public_url
    )
    db.session.add(application)
    db.session.commit()
    return jsonify(application.to_dict()), 201

# Get all applications for a job
@application_bp.route('/job/<int:job_id>', methods=['GET'])
def get_applications_for_job(job_id):
    applications = Application.query.filter_by(job_id=job_id).all()
    return jsonify([application.to_dict() for application in applications]), 200

# Update application status
@application_bp.route('/<int:application_id>', methods=['PATCH'])
def update_application_status(application_id):
    data = request.get_json()
    status = data.get('status')
    application = Application.query.get_or_404(application_id)
    application.status = status
    db.session.commit()
    return jsonify(application.to_dict()), 200
