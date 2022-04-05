"""Models for Flask Notes app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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




def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)