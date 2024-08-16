from flask import request, jsonify, current_app as app  # Add current_app for app context
from flask_restful import Resource, Api
from app.models import db, Application, Job
from app.utils import save_uploaded_file
from app.config import Config

def setup_routes(app):
    api = Api(app)
    api.add_resource(JobListAPI, '/api/jobs')
    api.add_resource(JobAPI, '/api/jobs/<int:job_id>')
    api.add_resource(JobApplicationAPI, '/api/job/apply')
    api.add_resource(ApplicationStatusAPI, '/api/application/status')

# Resource Classes
class JobApplicationAPI(Resource):
    def post(self):
        user_id = request.form.get('user_id')
        job_id = request.form.get('job_id')
        resume = request.files.get('resume')
        cover_letter = request.files.get('cover_letter')

        if not user_id or not job_id or not resume or not cover_letter:
            return jsonify({"error": "Missing required parameters"}), 400

        filename_resume = save_uploaded_file(resume, app.config['UPLOAD_FOLDER'])
        filename_cover_letter = save_uploaded_file(cover_letter, app.config['UPLOAD_FOLDER'])

        if not filename_resume or not filename_cover_letter:
            return jsonify({"error": "Invalid file type"}), 400

        application = Application(
            user_id=user_id,
            job_id=job_id,
            resume=filename_resume,
            cover_letter=filename_cover_letter
        )

        db.session.add(application)
        db.session.commit()

        return jsonify({"message": "Application submitted successfully"}), 201

class ApplicationStatusAPI(Resource):
    def get(self):
        user_id = request.args.get('user_id')
        job_id = request.args.get('job_id')

        application = Application.query.filter_by(user_id=user_id, job_id=job_id).first()
        if application:
            return jsonify({"status": application.status}), 200
        else:
            return jsonify({"error": "Application not found"}), 404

class JobListAPI(Resource):
    def get(self):
        jobs = Job.query.all()
        return jsonify([job.to_dict() for job in jobs])

    def post(self):
        data = request.get_json()
        job = Job(
            title=data.get('title'),
            description=data.get('description'),
            company_name=data.get('company_name'),
            location=data.get('location')
        )
        db.session.add(job)
        db.session.commit()
        return jsonify(job.to_dict()), 201

class JobAPI(Resource):
    def get(self, job_id):
        job = Job.query.get_or_404(job_id)
        return jsonify(job.to_dict())

    def put(self, job_id):
        job = Job.query.get_or_404(job_id)
        data = request.get_json()
        job.title = data.get('title', job.title)
        job.description = data.get('description', job.description)
        job.company_name = data.get('company_name', job.company_name)
        job.location = data.get('location', job.location)
        db.session.commit()
        return jsonify(job.to_dict())

    def delete(self, job_id):
        job = Job.query.get_or_404(job_id)
        db.session.delete(job)
        db.session.commit()
        return '', 204
