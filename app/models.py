from flask_sqlalchemy import SQLAlchemy
from firebase_admin import storage

db = SQLAlchemy()

class UserModel:
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(64), index=True, unique=True)
        email = db.Column(db.String(120), index=True, unique=True)
        password = db.Column(db.String(128))
        role = db.Column(db.String(128))

    @staticmethod
    def create_user(username, email, password):
        new_user = UserModel.User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def get_user(user_id):
        return UserModel.User.query.get(user_id)

    @staticmethod
    def update_user(user_id, updates):
        user = UserModel.get_user(user_id)
        if user:
            for key, value in updates.items():
                setattr(user, key, value)
            db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = UserModel.get_user(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

class JobModel:
    class Job(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(100), nullable=False)
        description = db.Column(db.Text, nullable=False)
        company_name = db.Column(db.String(100), nullable=False)
        location = db.Column(db.String(100), nullable=False)
        posted_date = db.Column(db.DateTime, default=db.func.current_timestamp())

        def to_dict(self):
            return {
                'id': self.id,
                'title': self.title,
                'description': self.description,
                'company_name': self.company_name,
                'location': self.location,
                'posted_date': self.posted_date.isoformat()
            }

    @staticmethod
    def add_job(title, description, company_name, location):
        new_job = JobModel.Job(title=title, description=description, company_name=company_name, location=location)
        db.session.add(new_job)
        db.session.commit()

    @staticmethod
    def get_jobs():
        return JobModel.Job.query.all()

    @staticmethod
    def get_job(job_id):
        return JobModel.Job.query.get(job_id)

    @staticmethod
    def update_job(job_id, updates):
        job = JobModel.get_job(job_id)
        if job:
            for key, value in updates.items():
                setattr(job, key, value)
            db.session.commit()
        return job

    @staticmethod
    def delete_job(job_id):
        job = JobModel.get_job(job_id)
        if job:
            db.session.delete(job)
            db.session.commit()

class ApplicationModel:
    class Application(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        resume = db.Column(db.String(128))
        cover_letter = db.Column(db.String(128))
        status = db.Column(db.String(64), default='submitted')
        job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @staticmethod
    def submit_application(user_id, job_id, resume_file, cover_letter_file):
        resume_url = ApplicationModel.upload_file(resume_file)
        cover_letter_url = ApplicationModel.upload_file(cover_letter_file)
        new_application = ApplicationModel.Application(
            resume=resume_url,
            cover_letter=cover_letter_url,
            job_id=job_id,
            user_id=user_id
        )
        db.session.add(new_application)
        db.session.commit()

    @staticmethod
    def get_application(application_id):
        return ApplicationModel.Application.query.get(application_id)

    @staticmethod
    def upload_file(file):
        bucket = storage.bucket()
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)
        return blob.public_url
