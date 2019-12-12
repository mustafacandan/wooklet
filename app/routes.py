import os
from flask import Blueprint, request, redirect, render_template, send_from_directory, url_for, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app.services.handlers import UserHandler, BookHandler

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditor, CKEditorField, upload_fail, upload_success

from flask import current_app
from app.forms import compose_form, signup_form, login_form, compose_page_form
bp = Blueprint('base', __name__)


@bp.context_processor
def context_processor():
    user_info = None
    if current_user.get_id():
        user_info = current_user.username
    general = {
        'user_info' : user_info
    }
    return dict(general=general)


@bp.route('/files/<filename>')
def uploaded_files(filename):
    path = current_app.config['UPLOADED_PATH']
    return send_from_directory(path, filename)


@bp.route('/upload', methods=['POST'])
@login_required
def upload():
    f = request.files.get('file')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join(current_app.config['UPLOADED_PATH'], f.filename))
    url = url_for('base.uploaded_files', filename=f.filename)

    return upload_success(url=url)


@bp.route('/', methods=['GET'])
def home():
    # get all public books from all authors
    return render_template('home.html'), 200


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = login_form()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    else:
        if form.validate_on_submit():
            user, err = UserHandler.check_user_information(form)
        if err:
            return 'incorrect information login', 400
        else:
            login_user(user, remember=True, force=True)
            return redirect(url_for('base.home'))


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('base.home'))


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = signup_form()
    if request.method == 'GET':
        return render_template('signup.html', form=form)
    else:
        if form.validate_on_submit():
            user = UserHandler.create_user(form)
            login_user(user, remember=True, force=True)
            return redirect(url_for('base.home'))
    return 'incorrect information signup', 400


@bp.route('/unauthorized', methods=['GET', 'POST'])
def unauthorized():
    return redirect(url_for('base.login'))


@bp.route('/books', methods=['GET', 'POST'])
@login_required
def book_list():
    if request.method == 'GET':
        books = BookHandler.get_books()
        return render_template('book_list.html', books=books)

# TODO: Delete Book


@bp.route('/compose/new', methods=['GET', 'POST'])
@login_required
def compose_new():
    form = compose_form()
    if request.method == 'GET':
        return render_template('compose_new.html', form=form)
    else:
        # creates a book
        book_id = BookHandler.create_book(request)
        res = {
            'action': 'new_path',
            'book_id': book_id
        }
        return jsonify(res), 200


@bp.route('/book/<book_name>/parts/<book_id>', methods=['GET', 'POST'])
@login_required
def compose_edit(book_name, book_id):
    form = compose_form()
    if request.method == 'GET':
        # get paths with book id
        paths = BookHandler.get_paths_by_book_id(book_id)

        data = {
            'paths': paths,
            'book_id': book_id
        }
        return render_template('book_parts.html', form=form, data=data)

@bp.route('/book/<book_name>/settings/<book_id>', methods=['GET'])
@login_required
def book_settings(book_id, book_name):
    return render_template('book_settings.html')

@bp.route('/book/<book_name>/pages/<path_id>', methods=['GET'], defaults={'page_id': 'new'})
@login_required
def list_pages_(page_id, path_id, book_name):
    form = compose_page_form()
    paths = BookHandler.get_paths(page_id=page_id, path_id=path_id)
    book_id = BookHandler.get_book(page_id=page_id, path_id=path_id)['id']
    pages = BookHandler.get_pages_by_path(path_id)
    data = {
        'pages': pages,
        'paths': paths,
        'page_id': page_id,
        'path_id': path_id,
        'book_id': book_id
    }
    return render_template('book_part_pages.html', form=form, data=data)

@bp.route('/book/<book_name>/page/new/<path_id>', methods=['GET'], defaults={'page_id': 'new'})
@bp.route('/book/<book_name>/page/<page_id>', methods=['GET'], defaults={'path_id': None})
@login_required
def book_part(page_id, path_id, book_name):
    print(path_id, end=' ###\n')
    form = compose_page_form()
    paths = BookHandler.get_paths(page_id=page_id, path_id=path_id)
    book_id = BookHandler.get_book(page_id=page_id, path_id=path_id)['id']
    page = ""
    if page_id != 'new':
        page = BookHandler.get_page_by_id(page_id)

    if not path_id:
        path_id = page['path_id']

    data = {
        'page': page,
        'paths': paths,
        'page_id': page_id,
        'path_id': path_id,
        'book_id': book_id
    }
    return render_template('compose_page.html', form=form, data=data)

@bp.route('/compose/<book_name>/page/new/<path_id>', methods=['GET'], defaults={'page_id': 'new'})
@bp.route('/compose/<book_name>/page/<page_id>', methods=['GET'], defaults={'path_id': None})
@login_required
def compose_n(page_id, path_id, book_name):
    print(path_id, end=' ###\n')
    form = compose_page_form()
    paths = BookHandler.get_paths(page_id=page_id, path_id=path_id)
    book_id = BookHandler.get_book(page_id=page_id, path_id=path_id)['id']
    page = ""
    if page_id != 'new':
        page = BookHandler.get_page_by_id(page_id)
    data = {
        'page': page,
        'paths': paths,
        'page_id': page_id,
        'path_id': path_id,
        'book_id': book_id
    }
    return render_template('compose_page.html', form=form, data=data)


@bp.route('/compose/<page_id>', methods=['GET', 'POST'])
@login_required
def compose(page_id):
    form = compose_page_form()
    if request.method == 'GET':
        data = {
            'page_id': page_id,
            'path_id': path_id
        }
        return render_template('compose_page.html', form=form, data=data)
    else:
        if request.args.get('action') == 'next':
            # this function creates new page obj and append it to path
            page_id = BookHandler.add_page(request)
            res = {
                'action': 'next',
                'page_id': page_id
            }
        elif request.args.get('action') == 'path':
            # this function creates new path obj and append it to the child and opens editor with that path id
            path_id = BookHandler.add_path(request)
            res = {
                'action': 'path',
                'page_id': path_id
            }
        elif request.args.get('action') == 'end':
            page_id = BookHandler.end_path(request)
            res = {
                'action': 'end',
                'page_id': ''
            }
        elif request.args.get('action') == 'connect':
            # page_id = BookHandler.connect_path(request)
            res = {
                'action': 'connect',
                'page_id': ''
            }
        else:
            return 403
        return jsonify(res), 200


@bp.route('/page/all/<path_id>', methods=['POST'])
@login_required
def get_pages(path_id):
    if request.method == 'POST':
        pages = BookHandler.get_pages_by_path(path_id)
        return jsonify(pages)


@bp.route('/page/save/<page_id>', methods=['GET', 'POST'])
@login_required
def sage_page(page_id):
    page = BookHandler.save_page(page_id, request)
    return jsonify({'page_id': page.id}), 200


@bp.route('/path/add/<parent_path_id>', methods=['POST'])
@login_required
def add_path(parent_path_id):
    path_name = 'Yeni Node'
    path = BookHandler.add_path(parent_path_id, path_name)
    path_id = path.get('id')
    return jsonify({'id': path_id}), 200


@bp.route('/path/rename/<path_id>', methods=['POST'])
@login_required
def rename_path(path_id):
    path = BookHandler.rename_path(path_id, request)
    return jsonify('success'), 200


@bp.route('/path/delete/<path_id>', methods=['POST'])
@login_required
def delete_path(path_id):
    path = BookHandler.delete_path(path_id)
    return jsonify('success'), 200


@bp.route('/tree/get/<book_id>', methods=['GET'])
@login_required
def get_tree(book_id):
    paths, err = BookHandler.get_tree(book_id)
    return jsonify(paths[0]), 200


@bp.route('/next', methods=['POST'])
@login_required
def next():
    # text = request.form.get('text')
    # saves the page and returns the next 
    return "", 200