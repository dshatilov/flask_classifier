from app import db


class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.String(64), index=True)
    text = db.Column(db.String(64), index=True)

    def __repr__(self):
        return 'id: {}, parent: {}, test: {}'.format(self.id, self.parent, self.text)
