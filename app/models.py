from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean)
    email = db.Column(db.String(120), index=True, unique=True)
    about_me = db.Column(db.String(140))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'password_hash': self.password_hash,
            'active': self.active,
            'email': self.email,
            'about_me': self.about_me

        }
        return data

    def from_dict(self, data):
        for field in ['username', 'password_hash', 'active', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def to_collection_dict(query):
        resultlist = query
        return {'items': [item.to_dict() for item in resultlist], }

    @staticmethod
    def find_by_id(id):
        return User.query.filter_by(id=id).first()

    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username).first()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_to_db(self):
        db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
