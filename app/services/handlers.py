from flask import current_app
from app import queries as q
from .exceptions import InvalidUsage

class UserHandler:
    @classmethod
    def create_user(cls, form):
        email = form.email.data
        username = form.username.data
        password = form.password.data
        if (username or email) and password:
            user_info = {
                'email' : email,
                'username' : username,
                'password' : password,
                'user_type': 'user'
            }
            return q.create_user(user_info)
        else:
            raise InvalidUsage('username or email didnt supply')

    @classmethod
    def check_user_information(cls, form):
        username = email = None
        if '@' in form.username_or_email.data:
            email = form.username_or_email.data
        else:
            username = form.username_or_email.data
        password = form.password.data
        if (username or email) and password:
            if username:
                user = q.get_user_by_username(username)
            if email:
                user = q.get_user_by_email(email)
            
            if user.check_password(password):
                return user, None
            else:
                return None, "Incorrect Password"

class FileHandler:
    @classmethod
    def ValidateImageType(extension):
        return extension in ['jpg', 'gif', 'png', 'jpeg']

    @classmethod
    def UploadFile():
        f = request.files.get('upload')
        extension = f.filename.split('.')[-1].lower()
        if extension not in ['jpg', 'gif', 'png', 'jpeg']:
            return upload_fail(message='Image only!')
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
        url = url_for('uploaded_files', filename=f.filename)
        return upload_success(url=url)