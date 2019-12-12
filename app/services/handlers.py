from flask import current_app
from app import queries as q
from .exceptions import InvalidUsage
from flask_login import current_user

class BookHandler:
    @classmethod
    def get_tree(cls, book_id):
        return q.get_paths_by_book_id(book_id)


    @classmethod
    def add_path(cls, parent_path_id, path_name):
        data, err = q.add_path(parent_path_id, path_name)
        if not err:
            return data
        else:
            print(err)
            return None

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

        return book.id

    @classmethod
    def get_book(cls, path_id=None, page_id=None, id=None):
        if id:
            return q.get_book_by_id(id)
        elif path_id:
            return q.get_book_by_path_id(path_id)
        elif page_id:
            return q.get_book_by_page_id(page_id)


    @classmethod
    def get_books(cls):
        user_id = current_user.get_id()
        if not user_id:
            raise InvalidUsage('Login needed')
        return q.get_books_by_user(user_id)

    @classmethod
    def get_paths_by_book_id(cls, book_id):
        data, err = q.get_paths_by_book_id(book_id)
        if not err:
            return data

    @classmethod
    def get_paths(cls, page_id, path_id):
        if path_id:
            data, err = q.get_paths_by_path_id(path_id)
        elif page_id != 'new':
            data, err = q.get_paths_by_page_id(page_id)

        if not err:
            return data


    @classmethod
    def save_page(cls, page_id, request):
        if page_id == 'new':
            # Create new page
            page_data = request.form.to_dict()
            path_id = page_data['path_id']
            page_raw = {
                'content': page_data['content']
            }
            page = q.create_page(path_id, page_raw)
            return page
        else:
            # Update existing page
            page_data = request.form.to_dict()
            page_id = page_data['page_id']
            page_raw = {
                'content': page_data['content']
            }
            return q.update_page(page_id, page_raw)

    @classmethod
    def delete_path(cls, id):
        data, _err = q.delete_path(id)
        if not _err:
            print(_err)
            return data


    @classmethod
    def rename_path(cls, id, request):
        name = request.form.get('name')
        data, _err = q.rename_path(id, name)
        if not _err:
            print(_err)
            return data

    @classmethod
    def end_path(cls, id):
        data, _err = q.end_path(id)
        if not _err:
            print(_err)
            return data

    @classmethod
    def get_page_by_id(cls, page_id):
        data, _err = q.get_page_by_id(page_id)
        if not _err:
            return data



    @classmethod
    def get_pages_by_path(cls, path_id):
        data, _err =  q.get_pages_by_path(path_id)
        if not _err:
            return data

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