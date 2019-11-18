import os
from flask import Blueprint, request, redirect, render_template, send_from_directory, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app.services.handlers import UserHandler, BookHandler

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditor, CKEditorField, upload_fail, upload_success

from flask import current_app
from app.forms import compose_form, signup_form, login_form
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

@bp.route('/', methods=['GET', 'POST'])
def home():
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
    return redirect(url_for('base.home'))



@bp.route('/unauthorized', methods=['GET', 'POST'])
def unauthorized():
    return redirect(url_for('base.login'))

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

@bp.route('/compose', methods=['GET', 'POST'])
@login_required
def book_list():
    if request.method == 'GET':
        # list all editable books
        books = [
            {
                'title': 'Baslik',
                'description': 'Kitapla ilgili aciklama yazisi',
                'status': 'draft'
            },  {
                'title': 'Baslik2',
                'description': '2 2Kitapla ilgili aciklama yazisi',
                'status': 'draft'
            },  {
                'title': 'Baslik2',
                'description': '2 2Kitapla ilgili aciklama yazisi',
                'status': 'draft'
            }
        ]
        # BookHandler.book
        return render_template('book_list.html', books=books)

@bp.route('/compose/new', methods=['GET', 'POST'])
@login_required
def compose_new():
    form = compose_form()
    if request.method == 'GET':
        
        return render_template('compose_new.html', form=form)
    else:
        if form.validate_on_submit():
            return redirect(url_for('base.home')), 200
        # create article
        # return

@bp.route('/next', methods=['POST'])
@login_required
def next():
    text = request.form.get('text')
    return "", 200