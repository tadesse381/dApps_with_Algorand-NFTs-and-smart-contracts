from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4


def get_uuid():
    return uuid4().hex

class User(db.Document):
    active = db.BooleanField(default=False)

    # User authentication information
    _password = db.StringField(required=True)
    email = db.StringField(unique=True, required=True)
    user_id = db.StringField(unique=True, default=get_uuid)
    address = db.StringField(unique=True)

    # User information
    first_name = db.StringField(default='')
    last_name = db.StringField(default='')

    # Relationships
    roles = db.StringField()
    email_confirmed_at = db.DateTimeField()

    def get_email(self):
        return self.email

    def get_user_id(self):
        return self.user_id

    @property
    def password(self):
        raise AttributeError("Can't read password")

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._password, password)
