from app import models as m

# USER FUNCTIONS
def create_user(user_info):
    username = user_info.get('username')
    email = user_info.get('email')
    user_type = user_info.get('user_type')
    password = user_info.get('password') # will add hashing

    new_user = m.User(username=username,
                    email=email,
                    user_type=user_type)  # Create an instance of the User class

    new_user.set_password(password)

    user_schema = m.UserSchema()
    user_data, user_err = user_schema.load(user_info)

    if user_err:
        print(user_err)
        return None
    else:
        m.db.session.add(new_user)  # Adds new User record to database
        m.db.session.commit()
        return new_user

def get_user_by_email(email):
    return m.User.query.filter_by(email=email).first()

def get_user_by_username(username):
    return m.User.query.filter_by(username=username).first()

# BOOK FUNCTIONS
def create_book(book_raw, user_id):
    book_schema = m.BookSchema()
    book_data, _err = book_schema.load(book_raw)

    book = m.Book()
    book.title = book_data['title']
    book.description = book_data['description']
    book.cover = book_data['cover']

    book.editors.append(m.User.query.get(user_id))

    if _err:
        return None
    else:
        m.db.session.add(book)
        m.db.session.commit()

    # book_dump = book_schema.dump(book)
    return book


def get_book_by_id(book_id):
    book = m.Book.query.get(book_id)
    data, err = m.BookSchema().dump(book)
    if not err:
        print(err)
        return data

def get_book_by_path_id(path_id):
    path = m.Path.query.get(path_id)

    print(path.book_id, end=" book id \n")

    book = m.Book.query.get(path.book_id)
    data, err = m.BookSchema().dump(book)
    if not err:
        print(err)
        return data


def get_book_by_page_id(page_id):
    page = m.Page.query.get(page_id)
    path = m.Path.query.get(page.path_id)
    book = m.Book.query.get(path.book_id)
    data, err = m.BookSchema().dump(book)
    if not err:
        return data

def get_books_by_user(user_id):
    books = m.Book.query.filter(m.Book.is_deleted.is_(False)).filter(m.Book.editors.any(id=user_id)).all()

    data, err = m.BookSchema().dump(books, many=True)
    print(data)
    if not err:
        return data


def get_public_books():
    books = m.Book.query.filter(m.Book.is_deleted.is_(False)).filter(m.Book.status == 'public').all()
    data = m.BookSchema().dump(books, many=True)
    return data

# PATH FUNCTIONS
def get_paths_by_book_id(book_id):
    paths = m.Path.query.filter(m.Path.book_id == book_id).filter(m.Path.parent.is_(None))
    print(book_id)
    return m.PathSchema().dump(paths, many=True)

def get_paths_by_path_id(path_id):
    path = m.Path.query.get(path_id)
    paths = m.Path.query.filter_by(book_id=path.book_id)
    return m.PathSchema().dump(paths, many=True)

def get_paths_by_page_id(page_id):
    page = m.Page.query.get(page_id)
    path = m.Path.query.get(page.path_id)
    paths = m.Path.query.filter_by(book_id=path.book_id)
    return m.PathSchema().dump(paths, many=True)

def create_path(book_id, path_raw={}):
    path_schema = m.PathSchema()
    path_data, _err = path_schema.load(path_raw)

    path = m.Path()
    path.book_id = book_id
    path.text = 'Giris'
    if _err:
        print(_err)
        return None
    else:
        print(path.__dict__)
        m.db.session.add(path)
        m.db.session.commit()
        return path


def get_children_by_page(page_id):
    path = m.Path.query.filter(m.Path.id == m.Page.query.get(page_id).path_id) \
        .first()
    return m.PathSchemaChildren().dump(path)


def get_tree(book_id):
    path = m.Path.query.filter(m.Book.id == book_id) \
        .first()
    return m.PathSchemaRoot().dump(path)

def add_path(parent_id, path_name):
    path = m.Path.query.get(parent_id)

    new_path = m.Path()
    new_path.text = path_name
    new_path.book_id = path.book_id

    m.db.session.add(new_path)
    m.db.session.commit()

    path.children.append(new_path)
    m.db.session.commit()

    return m.PathSchemaRoot().dump(new_path)

def delete_path(id):
    path = m.Path.query.get(id)
    path.old_parent = path.__dict__['parent']
    path.parent = None
    m.db.session.commit()
    return m.PathSchemaRoot().dump(path)

def rename_path(id, name):
    path = m.Path.query.get(id)
    path.text = name
    m.db.session.commit()
    return m.PathSchemaRoot().dump(path)

def end_path(id):
    path = m.Path.query.get(id)
    path.icon = 'fas fa-file'
    m.db.session.commit()
    return m.PathSchemaRoot().dump(path)


# PAGE FUNCTIONS
def create_page(path_id, page_raw):
    page_schema = m.PageSchema()
    page_data, _err = page_schema.load(page_raw)
    if _err:
        print(_err)
        return False
    page = m.Page()
    page.content = page_data['content']
    page.path_id = path_id

    m.db.session.add(page)
    m.db.session.commit()
    return page


def update_page(page_id, page_raw):
    print(page_raw)

    page_schema = m.PageSchema()
    page_data, _err = page_schema.load(page_raw)

    if _err:
        print(_err)
        return False

    page = m.Page.query.get(page_id)
    page.content = page_data['content']

    m.db.session.commit()
    return page


def get_page_by_id(page_id):
    page = m.Page.query.get(page_id)
    return m.PageSchema().dump(page)


def get_last_page_of_parent_path_by_page_id(page_id):
    path_id = m.Page.query.get(page_id).path_id
    parent_id = m.Path.query.get(path_id).parent
    return m.Page.query.filter_by(path_id=parent_id).order_by(m.Page.created_at.desc()).first()
    # return m.Path.query.filter(m.Path.id == parent_id).pages.order_by(m.Page.created_at.asc()).last()


def get_pages_by_path(path_id):
    pages = m.Page.query.filter_by(path_id=path_id).order_by(m.Page.created_at.asc()).all()
    return m.PageSchema().dump(pages, many=True)


def get_pages_by_page(page_id):
    pages = m.Page.query.filter_by(path_id=m.Page.query.get(page_id).path_id).order_by(m.Page.created_at.asc()).all()
    return m.PageSchema().dump(pages, many=True)


def get_pages_by_book(book_id):
    root_path = m.Path.query.filter(m.Path.book_id == book_id).filter(m.Path.parent.is_(None)).filter(
        m.Path.old_parent.is_(None)).first().id
    # m.Path.query.filter(m.Path.parent.is_(None)).filter(m.Path.old_parent.is_(None)).first().id
    pages = m.Page.query.filter_by(path_id=root_path).order_by(m.Page.created_at.asc()).all()
    print(pages)
    return m.PageSchema().dump(pages, many=True)
