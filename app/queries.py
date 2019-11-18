from app import models as m

def create_user(user_info):
    username = user_info.get('username')
    email = user_info.get('email')
    user_type = user_info.get('user_type')
    password = user_info.get('password') # will add hashing

    new_user = m.Users(username=username,
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
    return m.Users.query.filter_by(email=email).first()

def get_user_by_username(username):
    return m.Users.query.filter_by(username=username).first()

# create user
# get user info
# update user info
# forget password email and token
# delete user (deactive)