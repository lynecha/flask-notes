"""Models for Flask Notes app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    """ User """

    __tablename__ = "users"

    username = db.Column(db.String(20),
                   primary_key=True)
    password = db.Column(db.String(100),
                     nullable=False)
    email = db.Column(db.String(50),
                        nullable=False,
                        unique = True)
    first_name = db.Column(db.String(30),
                        nullable=False)
    last_name = db.Column(db.String(30),
                        nullable=False)


    def __repr__(self):
        """ Return user data """

        u = self

        return f"<Username: {u.username} Password: {u.password} Email: {u.email} Firstname: {u.first_name} Lastname: {u.last_name}"


    def serialize(self):
        """ Serialize to dictionary """

        return {
                "username": self.username,
                "password": self.password,
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name
        }

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd).decode('utf8')

        # return instance of user w/username and hashed pwd
        return cls(
            username=username,
            password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name
            )

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = cls.query.filter_by(username=username).one_or_none()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

