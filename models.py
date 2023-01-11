from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    verified = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now)

    def serialize(self): 
        return {
            "id": self.id,
            "username": self.username,
            "active": self.active,
            "verified": self.verified,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()