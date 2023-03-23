# models are made here
from config import app, db

class Account(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    notes = db.relationship('Notes', backref="account", cascade="all, delete-orphan")

    def __repr__(self):
        return f'{self.username}'

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(1000))
    account_id = db.Column(db.Integer, db.ForeignKey("account.user_id"))

    def __repr__(self):
        return f'{self.title}'

with app.app_context():
    db.create_all()