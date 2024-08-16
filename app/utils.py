import re
from werkzeug.utils import secure_filename
import os

def validate_email(email):
    """
    Validates an email address using a regular expression.
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def save_uploaded_file(file, upload_folder):
    """
    Saves an uploaded file to the specified folder.
    """
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return filename
    return None

def allowed_file(filename):
    """
    Checks if the file extension is allowed.
    """
    allowed_extensions = {'pdf', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
