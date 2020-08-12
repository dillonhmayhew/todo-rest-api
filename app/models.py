from app import app, db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    done = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(128))

    def __repr__(self):
        return f'<Task {self.id}: {self.done}>'