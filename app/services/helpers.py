import os, json
from flask import current_app
from config import Config


class Helper:
    @classmethod
    def getenv(cls, debug=False):
        environment = os.getenv('FLASK_CONFIG') or 'development'
        if debug:
            print('>> env: ' + environment)

        return environment

    @classmethod
    def replace_dictionary_values(cls, source, search=None, replace=''):
        for key, value in source.items():
            if value == search:
                source[key] = replace
        return source

    @classmethod
    def json_decode_dictionary_values(cls, source, fields=[]):
        for field in fields:
            if field in source:
                try:
                    source[field] = json.loads(source[field])
                except json.JSONDecodeError:
                    source[field] = None

        return source

    @classmethod
    def associate_by_key(cls, items, key):
        result = {}
        for item in items:
            result[item[key]] = item

        return result

    @classmethod
    def base_path(cls, path):
        try:
            return os.path.join(current_app.config.get('BASE_DIR'), path)
        except RuntimeError as e:
            print(f'Error in base path: {e}')
        return os.path.join(Config.BASE_DIR, path)

    @classmethod
    def is_file_exists(cls, path, is_media=False):
        if is_media:
            path = current_app.config.get('THUMBNAIL_MEDIA_ROOT') + '/' + path
        return os.path.isfile(path)

    @classmethod
    def allowed_file(cls, filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

    @classmethod
    def is_excel_file(cls, filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in ['xls', 'xlsx']

    @classmethod
    def is_image_file(cls, file):
        if isinstance(file, str):
            return file and '.' in file and (file.rsplit('.', 1)[1]).lower() in ['png', 'jpg', 'jpeg']
        else:
            return file and hasattr(file, 'filename') and '.' in file.filename and (
                file.filename.rsplit('.', 1)[1]).lower() in ['png', 'jpg', 'jpeg']

    @classmethod
    def ensure_boolean(cls, value):
        if isinstance(value, bool):
            return value
        elif isinstance(value, str) and value.lower() in ('yes', 'true', 't', '1', 'on'):
            return True
        else:
            return False

    @classmethod
    def reverse_dictionary(cls, d):
        return {v: k for (k, v) in d.items()}

    @classmethod
    def strip_if_str(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value

    @classmethod
    def ensure_str(cls, value):
        return '' if not value else str(value).strip()

    @classmethod
    def is_valid_uuid(cls, uuid_to_test, version=4):
        try:
            uuid_obj = uuid.UUID(uuid_to_test, version=version)
        except:
            return False

        return str(uuid_obj) == uuid_to_test


