from db import db

class DrugarModel(db.Model):
    __tablename__ = 'drugar'

    id = db.Column(db.Integer, primary_key=True)
    drugar = db.Column(db.String(80))
    username = db.Column(db.String(80))
    position = db.Column(db.String(80))

    def __init__(self, drugar, username, position):       
        self.drugar = drugar
        self.username = username
        self.position = position

    def json(self):
        return {'drugar': self.drugar, 'username': self.username, 'position': self.position}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_drugar(cls, drugar):
        return cls.query.filter_by(drugar=drugar).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()