import os
from datetime import datetime, timedelta
import jwt
from pytz import timezone
from server import db

ng_timezone = timezone('Africa/Lagos')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String(200), unique=True)
    phone = db.Column(db.String(15))
    password_hash = db.Column(db.String(200))
    ip = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    role = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return "<User {}>".format(self.firstname)

    def generate_auth_token(self):
        # Calculate the expiration time
        expiration_time = datetime.utcnow() + timedelta(days=30)
        # Create the token payload with the user ID and expiration time
        payload = {
            'id': self.id,
            'exp': expiration_time,
            'role': self.role
        }
        # Generate the token
        token = jwt.encode(
            payload, os.environ.get('SECRET_KEY'), algorithm='HS256')

        return token

    @staticmethod
    def verify_auth_token(token):
        if not token:
            return False
        try:
            payload = jwt.decode(token, os.environ.get('SECRET_KEY'),
                                 algorithms=['HS256'])
            user = User.query.filter(User.id == payload['id']).first()
            return user
        except jwt.ExpiredSignatureError:
            return False
        except jwt.DecodeError:
            return False

    def get_roles(self):
        return self.role

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class VerificationCodes(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer)
    code = db.Column(db.String(15))
    active = db.Column(db.Boolean)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
