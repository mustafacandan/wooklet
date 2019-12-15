import os
from flask import Blueprint, request, redirect, render_template, send_from_directory, url_for, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app.services.handlers import UserHandler, BookHandler
from werkzeug.exceptions import InternalServerError, Unauthorized, NotFound

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditor, CKEditorField, upload_fail, upload_success

from flask import current_app
from app.forms import ComposeForm, SignupForm, LoginForm, ComposePageForm
bp = Blueprint('base', __name__)


@bp.context_processor
def context_processor():
    user_info = current_user.username if current_user else None
    data = {
        'user_info': user_info
    }
    return dict(**data)


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
    data = {
        'popular_books': BookHandler.get_public_books()[:3]
    }
    print(data['popular_books'])
    return render_template('index.html', **data), 200


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    else:
        err = None
        if form.validate_on_submit():
            user, err = UserHandler.check_user_information(form)
        if err:
            raise InternalServerError()
        else:
            login_user(user, remember=True, force=True)
            return redirect(url_for('base.home'))


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('base.home'))


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'GET':
        return render_template('signup.html', form=form)
    else:
        if form.validate_on_submit():
            user = UserHandler.create_user(form)
            login_user(user, remember=True, force=True)
            return redirect(url_for('base.home'))
    raise Unauthorized()


@bp.route('/book/<book_name>/detail/<book_id>')
def book_landing(book_name, book_id):
    data = {
        'book': BookHandler.get_book(None, None, book_id)
    }
    return render_template('book-landing.html', **data)


@bp.route('/compose/new', methods=['GET', 'POST'])
@login_required
def compose_new():
    form = ComposeForm()
    if request.method == 'GET':
        data = {
            'book_id': None,
            'path_id': None,
            'page_id': None
        }
        return render_template('compose_new.html', form=form, **data)
    else:
        # creates a book
        book = BookHandler.create_book(request)
        res = {
            'book_id': book.id,
            'book_title': book.title
        }
        return jsonify(res), 200


@bp.route('/my-books', methods=['GET', 'POST'])
@login_required
def book_list():
    if request.method == 'GET':
        books = BookHandler.get_books()
        return render_template('my-books.html', books=books)

# TODO: Delete Book


@bp.route('/book/<book_name>/read/<book_id>', defaults={'page_id': None, 'path_id': None})
@bp.route('/book/<book_name>/o/<path_id>', defaults={'book_id': None, 'page_id': None})
@bp.route('/book/<book_name>/<any(p, c, n):direction>/<page_id>', defaults={'book_id': None, 'path_id': None})
def read_book(book_name, book_id, page_id, path_id, direction='c'):
    if page_id:
        pages = BookHandler.get_pages_by_page(page_id)
    elif path_id:
        pages = BookHandler.get_pages_by_path(path_id)
    else:
        pages = BookHandler.get_pages_by_book(book_id)

    # if page id none return first page
    # iterate over pages
    # if matches with page_id return +1
    # if list ends show childrens

    page, options, parent_page = None, None, None
    data = {}

    # If page id doesnt exist, return first page
    if len(pages) > 0 and page_id is None:
        page = pages[0]
        data['title'] = BookHandler.get_book(page_id=page['id']).get('title')

    # if page id exist
    elif len(pages) > 0 and page_id:
        data['title'] = BookHandler.get_book(page_id=page_id).get('title')
        for i, p in enumerate(pages):
            if p['id'] == page_id:
                if direction == 'p' and i >= 1:
                    page = pages[i - 1]
                elif direction == 'c':
                    page = pages[i]
                elif direction == 'n':
                    if i <= len(pages) - 2:
                        page = pages[i+1]
                    elif i == len(pages) - 1:
                        data['prev_page_id'] = pages[i].get('id')
                        options = BookHandler.get_children_by_page(page_id)


    data['page'] = page
    data['options'] = options
    return render_template('read.html', **data)


@bp.route('/book/<book_name>/parts/<book_id>', methods=['GET', 'POST'])
@login_required
def compose_edit(book_name, book_id):
    form = ComposeForm()
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
    form = ComposePageForm()
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
    form = ComposePageForm()
    paths = BookHandler.get_paths(page_id=page_id, path_id=path_id)
    book_id = BookHandler.get_book(page_id=page_id, path_id=path_id)['id']
    page = None
    if page_id != 'new':
        page = BookHandler.get_page_by_id(page_id)

    if not path_id:
        print(page, end=' page \n')
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
    form = ComposePageForm()
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
    form = ComposePageForm()
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

@bp.route('/path/end/<path_id>', methods=['POST'])
@login_required
def end_path(path_id):
    path = BookHandler.end_path(path_id)
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


@bp.route('/unauthorized', methods=['GET'])
def unauthorized():
    data = {
        'title': 'Need Permission',
        'message': 'Apparently you don\'t have permission for this page'
    }
    return render_template('error.html', **data), 403


@bp.route('/400',)
def url_for_404():
    raise NotFound()


@bp.route('/500',)
def url_for_500():
    raise InternalServerError()


@bp.app_errorhandler(404)
def handle_404(err):
    user_info = current_user.username if current_user else None
    data = {
        'user_info': user_info
    }
    return render_template('404.html', **data), 404


@bp.app_errorhandler(500)
def handle_500(err):
    user_info = current_user.username if current_user else None
    data = {
        'user_info': user_info,
        'title': 'Something went wrong',
        'message': '(But don\'t worry we will take care of it.)'
    }
    return render_template('error.html', **data), 500
