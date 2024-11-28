from app import db
from datetime import datetime


class ProblemSolving(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    suggestion = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='problem_solving')

    def __repr__(self):
        return f'<ProblemSolving {self.id}>'
