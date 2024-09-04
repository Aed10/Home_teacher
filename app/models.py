from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    progress_data = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return f"<Progress {self.user_id}>"
