from flask import Blueprint, request, jsonify
from app.models import UserModel, JobModel, ApplicationModel, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

bp = Blueprint('api', __name__)

# User Routes
@bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    UserModel.create_user(data['username'], data['email'], data['password_hash'])
    return jsonify({'status': 'User created'}), 201

@bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user = get_jwt_identity()
    if current_user['id'] != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    user = UserModel.get_user(user_id)
    if user:
        return jsonify({
            'username': user.username,
            'email': user.email
        })
    else:
        return jsonify({'error': 'User not found'}), 404

# Job Routes
@bp.route('/jobs', methods=['POST'])
@jwt_required()
def create_job():
    data = request.json
    JobModel.add_job(data['title'], data['description'], data['company_name'], data['location'])
    return jsonify({'status': 'Job created'}), 201

@bp.route('/jobs', methods=['GET'])
def list_jobs():
    jobs = JobModel.get_jobs()
    return jsonify([job.to_dict() for job in jobs])

@bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job_by_id(job_id):
    job = JobModel.get_job(job_id)
    if job:
        return jsonify(job.to_dict())
    else:
        return jsonify({'error': 'Job not found'}), 404
    
@bp.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    data = request.json
    job = JobModel.get_job(job_id)
    if job:
        job.title = data.get('title', job.title)
        job.description = data.get('description', job.description)
        job.company_name = data.get('company_name', job.company_name)
        job.location = data.get('location', job.location)
        db.session.commit()
        return jsonify({'status': 'Job updated'}), 200
    else:
        return jsonify({'error': 'Job not found'}), 404
    
@bp.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    job = JobModel.get_job(job_id)
    if job:
        db.session.delete(job)
        db.session.commit()
        return jsonify({'status': 'Job deleted'}), 200
    else:
        return jsonify({'error': 'Job not found'}), 404
    
@bp.route('/jobs/search', methods=['GET'])
def search_jobs():
    query = request.args.get('query', '')
    jobs = JobModel.Job.query.filter(
        (JobModel.Job.title.ilike(f'%{query}%')) |
        (JobModel.Job.description.ilike(f'%{query}%')) |
        (JobModel.Job.company_name.ilike(f'%{query}%')) |
        (JobModel.Job.location.ilike(f'%{query}%'))
    ).all()
    return jsonify([job.to_dict() for job in jobs])


# Application Routes
@bp.route('/applications', methods=['POST'])
@jwt_required()
def submit_application():
    user_id = request.form['user_id']
    job_id = request.form['job_id']
    resume = request.files['resume']
    cover_letter = request.files['cover_letter']
    ApplicationModel.submit_application(user_id, job_id, resume, cover_letter)
    return jsonify({'status': 'Application submitted'}), 201

@bp.route('/applications/<int:application_id>', methods=['GET'])
@jwt_required()
def get_application(application_id):
    application = ApplicationModel.get_application(application_id)
    if application:
        return jsonify({
            'resume': application.resume,
            'cover_letter': application.cover_letter,
            'status': application.status,
            'job_id': application.job_id,
            'user_id': application.user_id
        })
    else:
        return jsonify({'error': 'Application not found'}), 404

@bp.route('/applications/user/<int:user_id>', methods=['GET'])
@jwt_required()
def list_user_applications(user_id):
    current_user = get_jwt_identity()
    if current_user['id'] != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    applications = ApplicationModel.Application.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'resume': app.resume,
        'cover_letter': app.cover_letter,
        'status': app.status,
        'job_id': app.job_id
    } for app in applications])

# Authentication Routes
@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = UserModel.User.query.filter_by(username=data['username']).first()
    if user and user.password_hash == data['password_hash']:
        access_token = create_access_token(identity={'id': user.id, 'username': user.username})
        return jsonify({'access_token': access_token})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
