from app import models as m

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

def create_path(book_id, path_raw={}):
    print('path creating')
    path_schema = m.PathSchema()

    path_data, _err = path_schema.load(path_raw)

    path = m.Path()
    path.book_id = book_id

    if _err:
        print(_err)
        return None
    else:
        print(path.__dict__)
        m.db.session.add(path)
        m.db.session.commit()
        return path