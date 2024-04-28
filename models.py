from datetime import datetime

from server import db


class UploadedMedia(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    filename = db.Column(db.String(200))
    uploaded = db.Column(db.DateTime, default=datetime.now())
    downloadUrl = db.Column(db.Text)
    mimetype = db.Column(db.String(10))
    user_id = db.Column(db.Integer)
    path = db.Column(db.Text)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
