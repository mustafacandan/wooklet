from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from sqlalchemy.dialects.postgresql import UUID, JSONB
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'))
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.now(), onupdate=db.func.now())
    is_deleted = db.Column(db.Boolean, nullable=False, index=True, default=False, server_default=db.text('false'))


class BaseSchema(Schema):
    id = fields.UUID(required=True, allow_none=False, dump_only=True)
    updated_at = fields.Date(required=True, allow_none=False, dump_only=True)


class User(BaseModel, UserMixin):
    is_active = db.Column(db.Boolean, nullable=False, default=True, server_default=db.text('true'))
    is_verified = db.Column(db.Boolean, nullable=True, default=False, server_default=db.text('false'))    
    user_type = db.Column(db.String(20), nullable=False, server_default="user")
    username = db.Column(db.String(120), nullable=True, unique=True)
    email = db.Column(db.String(120), nullable=True, unique=True)
    password = db.Column(db.String(120), nullable=False, index=False)
    full_name = db.Column(db.String(120), nullable=True, index=True)
    gsm = db.Column(db.String(30), nullable=True, index=True)
    gender = db.Column(db.String(10), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    photo_profile = db.Column(db.String(250), nullable=True, index=False)

    # relations
    books = db.relationship('Book', secondary='ownership', backref=db.backref('book_editors', lazy=True))

    def set_password(self, pwd):
        self.password = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)    

class UserSchema(BaseSchema):
    is_active = fields.Bool(required=False, allow_none=True)
    is_verified = fields.Bool(required=False, allow_none=False)
    user_type = fields.Str(required=False, allow_none=False)
    username = fields.Str(required=False, allow_none=True, unique=True)
    email = fields.Str(required=False, allow_none=True)
    password = fields.Str(required=True, allow_none=False, load_only=True)
    full_name = fields.Str(required=False, allow_none=False)
    gsm = fields.Str(required=False, allow_none=True)
    gender = fields.Str(required=False, allow_none=True)
    date_of_birth = fields.Date(required=False, allow_none=True)
    photo_profile = fields.Str(required=False, allow_none=True)
    books = fields.Nested('BookSchema', dump_only=True, many=True)

class EditorSchema(BaseSchema):
    is_active = fields.Bool(required=False, allow_none=True)
    is_verified = fields.Bool(required=False, allow_none=False)
    user_type = fields.Str(required=False, allow_none=False)
    username = fields.Str(required=False, allow_none=True, unique=True)
    email = fields.Str(required=False, allow_none=True)
    password = fields.Str(required=True, allow_none=False, load_only=True)
    full_name = fields.Str(required=False, allow_none=False)
    gsm = fields.Str(required=False, allow_none=True)
    gender = fields.Str(required=False, allow_none=True)
    date_of_birth = fields.Date(required=False, allow_none=True)
    photo_profile = fields.Str(required=False, allow_none=True)

class Book(BaseModel):
    cover = db.Column(db.String(256), nullable=True, index=False)
    title = db.Column(db.String(120), nullable=True, index=True)
    status = db.Column(db.String(25), nullable=False, index=False, server_default='draft')
    description = db.Column(db.String(3000), nullable=True, index=True)
    information = db.Column(JSONB(astext_type=db.Text()), nullable=True, index=True)

    # relations
    root_path = db.relationship('Path', backref=db.backref('root_path_book', lazy=True), uselist=False)
    editors = db.relationship('User', secondary='ownership', backref=db.backref('editor_books', lazy=True))


class BookSchema(BaseSchema):
    root_path_id = fields.UUID(required=False, allow_none=True)
    cover = fields.Str(required=False, allow_none=True)
    title = fields.Str(required=False, allow_none=True)
    status = fields.Str(required=False, allow_none=True)
    description = fields.Str(required=False, allow_none=True)
    information = fields.Dict(required=False, allow_none=True)
    editors = fields.Nested('EditorSchema', dump_only=True, many=True)
    created_at = fields.DateTime('%Y-%m-%d')
    updated_at = fields.DateTime('%Y-%m-%d')

class Ownership(BaseModel):
    is_owner = db.Column(db.Boolean, nullable=False, index=False, default=True, server_default=db.text('true'))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False, index=True)
    book_id = db.Column(UUID(as_uuid=True), db.ForeignKey('book.id'), nullable=False, index=True)


class Path(BaseModel):
    book_id = db.Column(UUID(as_uuid=True), db.ForeignKey('book.id'), nullable=True)
    text = db.Column(db.String(256), nullable=True, index=False)
    icon = db.Column(db.String(256), nullable=True, index=False, server_default='far fa-file-alt')

    parent = db.Column(UUID(as_uuid=True), db.ForeignKey('path.id'), nullable=True)
    old_parent = db.Column(UUID(as_uuid=True), nullable=True)

    # relations
    parent_id = db.relationship('Path', backref=db.backref('children', lazy=True),
                             uselist=False, remote_side='Path.id')

    pages = db.relationship('Page', backref=db.backref('path', lazy=True), uselist=False)


class PathSchema(BaseSchema):
    book_id = fields.UUID(required=False, allow_none=True)
    text = fields.Str(required=False, allow_none=True)
    icon = fields.Str(required=False, allow_none=True)
    children = fields.Nested('PathSchema', dump_only=True, many=True)


class PathSchemaLast(BaseSchema):
    class Meta:
        exclude = ('created_at', 'updated_at', 'parent_id')
    text = fields.Str(required=False, allow_none=True)


class PathSchemaChildren(BaseSchema):
    class Meta:
        exclude = ('created_at', 'updated_at', 'parent_id')
    text = fields.Str(required=False, allow_none=True)
    children = fields.Nested('PathSchemaLast', dump_only=True, many=True)


class PathSchemaRoot(BaseSchema):
    class Meta:
        exclude = ('created_at', 'updated_at', 'parent_id')
    text = fields.Str(required=False, allow_none=True)
    children = fields.Nested('PathSchemaRoot', dump_only=True, many=True)


class Page(BaseModel):
    content = db.Column(db.Text, nullable=True)
    path_id = db.Column(UUID(as_uuid=True), db.ForeignKey('path.id'), nullable=False)


class PageSchema(BaseSchema):
    content = fields.Str(required=True, allow_none=True)
    path_id = fields.UUID(required=False, allow_none=True)
