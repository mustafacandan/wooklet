import sys

import click
from flask import current_app
from flask.cli import AppGroup
from sqlalchemy import text

from app import models as m

cli = AppGroup('tune')


@cli.command('db')
@click.argument('command_name')
def create_user(command_name):
    if command_name == 'post-init':
        try:
            sql = text('CREATE EXTENSION pgcrypto;')
            result = m.db.engine.execute(sql)
        except:
            exc = sys.exc_info()
            print(exc)

        file_path = current_app.config.get('BASE_DIR') + '/migrations/script.py.mako'
        content = open(file_path).read()

        if 'import sqlalchemy_utils' not in content and 'import sqlalchemy as sa' in content:
            content = content.replace('import sqlalchemy as sa', 'import sqlalchemy as sa\nimport sqlalchemy_utils')

        f = open(file_path, 'w')
        f.write(content)
        f.close()