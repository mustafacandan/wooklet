from flask import current_app
from app import queries as q
from .exceptions import InvalidUsage
from flask_login import current_user

class BookHandler:
    @classmethod
    def create_book(cls, request):
        title = request.form.get('title')
        description = request.form.get('text')
        cover = request.form.get('cover')
        book_data = {
            'title': title,
            'description': description,
            'cover': cover
        }
        user_id = current_user.get_id()
        if not user_id:
            raise InvalidUsage('Login needed')

        book = q.create_book(book_data, user_id)
        if not book:
            raise InvalidUsage('book error')

        path = q.create_path(book.id)
        if not path:
            raise InvalidUsage('path error')

        return path.id

    @classmethod
    def get_book(cls, id):
        return q.get_book_by_id(id)

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
            
            if user:
                if user.check_password(password):
                    return user, None
            else:
                return None, "Incorrect Information"

class FileHandler:
    @classmethod
    def ValidateImageType(extension):
        return extension in ['jpg', 'gif', 'png', 'jpeg']